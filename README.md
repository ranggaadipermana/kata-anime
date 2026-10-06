# 🎌 Kata Anime Multilingual Dataset (Public API Ready)

Dataset kutipan anime multibahasa yang siap digunakan untuk keperluan REST API publik, aplikasi mobile, web, dan bot Discord/Telegram.

## 📂 Struktur Direktori

```text
.
├── kata-anime-indonesia.json          # File utama Bahasa Indonesia (legacy/root)
├── data/
│   ├── id/
│   │   └── kata-anime-indonesia.json   # 🇮🇩 Bahasa Indonesia (1.921 kutipan)
│   ├── en/
│   │   └── kata-anime-english.json     # 🇬🇧 English (1.921 kutipan)
│   ├── ja/
│   │   └── kata-anime-japanese.json    # 🇯🇵 Japanese (1.921 kutipan)
│   ├── tl/
│   │   └── kata-anime-filipino.json    # 🇵🇭 Filipino / Tagalog (1.921 kutipan)
│   └── ms/
│       └── kata-anime-malaysian.json   # 🇲🇾 Bahasa Melayu (1.921 kutipan)
└── README.md
```

---

## 📋 Skema JSON Data

Setiap data objek memiliki skema yang seragam dan konsisten di seluruh bahasa:

```json
{
  "character": "Mayoi Hachikuji",
  "quotes": "Wajar kalau siswa SMP itu (masih) anak-anak, masalahnya mereka tidak sadar kalau mereka anak-anak. Meskipun begitu masih lebih baik daripada orang dewasa yang tidak menganggap dirinya dewasa.",
  "anime": "Nisemonogatari",
  "episode": 6,
  "category": [
    "Dewasa",
    "Anak-anak"
  ]
}
```

### Penjelasan Bidang (Field):
| Field | Tipe | Deskripsi |
| :--- | :--- | :--- |
| `character` | `string` | Nama karakter dalam ejaan Romaji baku (konsisten antar bahasa untuk query relasional). |
| `quotes` | `string` | Teks kutipan yang telah disesuaikan dan diterjemahkan ke bahasa target. |
| `anime` | `string` | Judul anime dalam ejaan resmi/Romaji (konsisten antar bahasa). |
| `episode` | `number \| null` | Nomor episode tempat kutipan muncul. |
| `category` | `string[]` | Kategori tema kutipan yang diterjemahkan ke bahasa target. |

---

## 🌐 Contoh Penggunaan di Aplikasi / API Publik

### 1. Akses Langsung Melalui CDN GitHub (jsDelivr / Raw)
```javascript
// Contoh fetch dataset Bahasa Inggris via CDN
const url = 'https://cdn.jsdelivr.net/gh/ranggaadipermana/kata-anime@main/data/en/kata-anime-english.json';

async function getRandomQuote() {
  const response = await fetch(url);
  const data = await response.json();
  const random = data[Math.floor(Math.random() * data.length)];
  console.log(`"${random.quotes}" - ${random.character} (${random.anime})`);
}
```

### 2. Node.js / Express API Endpoint
```javascript
const express = require('express');
const app = express();

const datasets = {
  id: require('./data/id/kata-anime-indonesia.json'),
  en: require('./data/en/kata-anime-english.json'),
  ja: require('./data/ja/kata-anime-japanese.json'),
  tl: require('./data/tl/kata-anime-filipino.json'),
  ms: require('./data/ms/kata-anime-malaysian.json')
};

// Endpoint: /api/quotes?lang=en&category=Inspiration
app.get('/api/quotes/random', (req, res) => {
  const lang = req.query.lang || 'id';
  const data = datasets[lang] || datasets['id'];
  const randomQuote = data[Math.floor(Math.random() * data.length)];
  res.json(randomQuote);
});
```

---

## 📊 Statistik Dataset
- **Total Kutipan**: 1.921 per bahasa (Total: 9.605 kutipan lintas bahasa)
- **Kategori Unik**: ~1.309 kategori
- **Bahasa yang Didukung**: 5 Bahasa (Indonesia, English, Japanese, Filipino, Malaysian)
