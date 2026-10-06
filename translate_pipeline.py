import os
import sys
import json
import time
import shutil
import translators as ts
from deep_translator import MyMemoryTranslator

sys.stdout.reconfigure(encoding='utf-8')

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_FILE = os.path.join(WORKSPACE_DIR, 'kata-anime-indonesia.json')
DATA_DIR = os.path.join(WORKSPACE_DIR, 'data')
CACHE_DIR = os.path.join(WORKSPACE_DIR, '.cache_trans')

os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

LANGUAGES = {
    'en': {
        'name': 'English',
        'subfolder': 'en',
        'filename': 'kata-anime-english.json',
        'ts_code': 'en',
        'mm_code': 'en-US'
    },
    'ja': {
        'name': 'Japanese',
        'subfolder': 'ja',
        'filename': 'kata-anime-japanese.json',
        'ts_code': 'ja',
        'mm_code': 'ja-JP'
    },
    'tl': {
        'name': 'Filipino',
        'subfolder': 'tl',
        'filename': 'kata-anime-filipino.json',
        'ts_code': 'fil',
        'mm_code': 'tl-PH'
    },
    'ms': {
        'name': 'Malaysian',
        'subfolder': 'ms',
        'filename': 'kata-anime-malaysian.json',
        'ts_code': 'ms',
        'mm_code': 'ms-MY'
    }
}

DELIMITER = "\n===\n"

def translate_single(text, lang_cfg, max_retries=3):
    if not text or not text.strip():
        return text
    
    ts_code = lang_cfg['ts_code']
    mm_code = lang_cfg['mm_code']
    
    for engine in ['bing', 'alibaba']:
        for attempt in range(max_retries):
            try:
                res = ts.translate_text(text, from_language='id', to_language=ts_code, translator=engine)
                if res and res.strip():
                    return res.strip()
            except Exception:
                time.sleep(0.4 * (attempt + 1))
    
    # Fallback to MyMemory
    try:
        res = MyMemoryTranslator(source='id-ID', target=mm_code).translate(text)
        if res and res.strip():
            return res.strip()
    except Exception:
        pass
    
    return text

def translate_batch_quotes(quotes_chunk, lang_cfg):
    combined = DELIMITER.join(quotes_chunk)
    ts_code = lang_cfg['ts_code']
    
    for engine in ['bing', 'alibaba']:
        try:
            res = ts.translate_text(combined, from_language='id', to_language=ts_code, translator=engine)
            if res and res.strip():
                parts = [p.strip() for p in res.split('===') if p.strip()]
                if len(parts) == len(quotes_chunk):
                    return parts
        except Exception:
            time.sleep(0.3)
            
    # Fallback individual
    results = []
    for q in quotes_chunk:
        results.append(translate_single(q, lang_cfg))
        time.sleep(0.1)
    return results

def load_cache(lang_code):
    cache_file = os.path.join(CACHE_DIR, f"cache_{lang_code}.json")
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                quotes_cache = {}
                # Clean bad fallback entries
                for k, v in data.get('quotes', {}).items():
                    if v and v.strip():
                        # If for non-ms it's identical to original, drop it so we re-translate properly
                        if lang_code != 'ms' and k.strip() == v.strip():
                            continue
                        quotes_cache[k] = v
                cats_cache = {}
                for k, v in data.get('categories', {}).items():
                    if v and v.strip():
                        cats_cache[k] = v
                return {'quotes': quotes_cache, 'categories': cats_cache}
        except Exception as e:
            print(f"[{lang_code}] Cache read error: {e}, starting fresh")
    return {'quotes': {}, 'categories': {}}

def save_cache_safe(lang_code, cache_data):
    cache_file = os.path.join(CACHE_DIR, f"cache_{lang_code}.json")
    for attempt in range(5):
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            return
        except PermissionError:
            time.sleep(0.5)
        except Exception as e:
            time.sleep(0.5)

def translate_categories_all(categories, lang_code, lang_cfg, cache):
    print(f"[{lang_code}] Mengecek kategori ({len(categories)} kategori unik)...")
    cats_to_trans = [c for c in categories if c not in cache['categories']]
    print(f"[{lang_code}] Kategori yang perlu diterjemahkan: {len(cats_to_trans)}")

    if not cats_to_trans:
        return

    batch_size = 25
    for i in range(0, len(cats_to_trans), batch_size):
        chunk = cats_to_trans[i:i + batch_size]
        combined = '\n'.join(chunk)
        success = False
        for engine in ['bing', 'alibaba']:
            try:
                res = ts.translate_text(combined, from_language='id', to_language=lang_cfg['ts_code'], translator=engine)
                lines = [l.strip() for l in res.split('\n') if l.strip()]
                if len(lines) == len(chunk):
                    for orig, tr in zip(chunk, lines):
                        cache['categories'][orig] = tr
                    success = True
                    break
            except Exception:
                time.sleep(0.2)
        
        if not success:
            for c in chunk:
                cache['categories'][c] = translate_single(c, lang_cfg)
                time.sleep(0.1)

        save_cache_safe(lang_code, cache)
        if (i // batch_size) % 10 == 0 or i + batch_size >= len(cats_to_trans):
            print(f"[{lang_code}] Progres kategori: {min(i + batch_size, len(cats_to_trans))}/{len(cats_to_trans)}")
        time.sleep(0.2)

    save_cache_safe(lang_code, cache)
    print(f"[{lang_code}] Selesai kategori.")

def translate_quotes_all(quotes_list, lang_code, lang_cfg, cache):
    print(f"[{lang_code}] Mengecek quotes ({len(quotes_list)} kutipan)...")
    needed = [q for q in quotes_list if q not in cache['quotes']]
    print(f"[{lang_code}] Quotes yang perlu diterjemahkan: {len(needed)}")

    if not needed:
        return

    total = len(needed)
    completed = 0
    start_time = time.time()
    batch_size = 5

    for i in range(0, total, batch_size):
        chunk = needed[i:i + batch_size]
        translated_chunk = translate_batch_quotes(chunk, lang_cfg)
        
        for q, tr in zip(chunk, translated_chunk):
            cache['quotes'][q] = tr
            completed += 1

        save_cache_safe(lang_code, cache)

        elapsed = time.time() - start_time
        speed = completed / elapsed if elapsed > 0 else 0
        rem = (total - completed) / speed if speed > 0 else 0
        print(f"[{lang_code}] Progres quotes: {completed}/{total} ({completed*100/total:.1f}%) - Speed: {speed:.1f} q/s - ETA: {rem:.0f}s")
        time.sleep(0.3)

    save_cache_safe(lang_code, cache)
    print(f"[{lang_code}] Selesai quotes.")

def build_language_dataset(source_data, lang_code, config):
    cache = load_cache(lang_code)

    all_categories = []
    for item in source_data:
        if isinstance(item.get('category'), list):
            for c in item['category']:
                c_clean = c.strip()
                if c_clean and c_clean not in all_categories:
                    all_categories.append(c_clean)

    translate_categories_all(all_categories, lang_code, config, cache)

    all_quotes = []
    for item in source_data:
        q = item.get('quotes', '')
        if q and q not in all_quotes:
            all_quotes.append(q)

    translate_quotes_all(all_quotes, lang_code, config, cache)

    # Build target JSON
    target_dir = os.path.join(DATA_DIR, config['subfolder'])
    os.makedirs(target_dir, exist_ok=True)
    target_path = os.path.join(target_dir, config['filename'])

    translated_data = []
    for item in source_data:
        orig_quote = item.get('quotes', '')
        trans_quote = cache['quotes'].get(orig_quote, orig_quote)
        
        orig_cats = item.get('category', [])
        trans_cats = [cache['categories'].get(c.strip(), c.strip()) for c in orig_cats]

        new_item = {
            "character": item.get("character"),
            "quotes": trans_quote,
            "anime": item.get("anime"),
            "episode": item.get("episode"),
            "category": trans_cats
        }
        translated_data.append(new_item)

    # Save final JSON directly
    with open(target_path, 'w', encoding='utf-8') as f:
        json.dump(translated_data, f, ensure_ascii=False, indent=2)

    print(f"[{lang_code}] File JSON selesai disimpan: {target_path} ({len(translated_data)} data)")

def main():
    print("Membaca data sumber kata-anime-indonesia.json...")
    with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
        source_data = json.load(f)

    print(f"Total data: {len(source_data)} kutipan.")

    # 1. Pastikan data id tersimpan di data/id/kata-anime-indonesia.json
    id_dir = os.path.join(DATA_DIR, 'id')
    os.makedirs(id_dir, exist_ok=True)
    id_target = os.path.join(id_dir, 'kata-anime-indonesia.json')
    with open(id_target, 'w', encoding='utf-8') as f:
        json.dump(source_data, f, ensure_ascii=False, indent=2)
    print(f"[id] Data Indonesia tersimpan di {id_target}")

    # 2. Proses masing-masing bahasa
    for lang_code, config in LANGUAGES.items():
        print(f"\n==========================================")
        print(f"MEMPROSES: {config['name']} ({lang_code})")
        print(f"==========================================")
        build_language_dataset(source_data, lang_code, config)

    print("\n==========================================")
    print("SEMUA DATASET BERHASIL DITERJEMAHKAN!")
    print("==========================================")

if __name__ == '__main__':
    main()
