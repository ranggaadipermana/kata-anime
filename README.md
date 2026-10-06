# 🎌 Kata Anime Multilingual Dataset (Public API Ready)

<p align="center">
  <img src="https://img.shields.io/badge/Total%20Quotes-9%2C605-ff69b4?style=for-the-badge&logo=quote" alt="Total Quotes" />
  <img src="https://img.shields.io/badge/Languages-5%20Supported-4169e1?style=for-the-badge&logo=google-translate" alt="Languages" />
  <img src="https://img.shields.io/badge/Format-JSON-brightgreen?style=for-the-badge&logo=json" alt="Format" />
  <img src="https://img.shields.io/badge/License-MIT-orange?style=for-the-badge" alt="License" />
</p>

---

## 📖 Tentang Proyek (About)

**Kata Anime Multilingual Dataset** adalah basis data terbuka (*open dataset*) yang menghimpun ribuan kutipan bijak, inspiratif, emosional, dan bermakna dari berbagai judul anime populer ke dalam 5 bahasa: **Bahasa Indonesia**, **Bahasa Inggris**, **Bahasa Jepang**, **Bahasa Filipina (Tagalog)**, dan **Bahasa Malaysia (Melayu)**.

Proyek ini dibangun sebagai sumber data (*single source of truth*) yang siap dikonsumsi langsung untuk pengembangan:
- 🚀 **REST API Publik** (Node.js, Python FastAPI/Flask, Go, PHP, dsb.)
- 📱 **Aplikasi Mobile** (Flutter, React Native, Swift, Kotlin)
- 🤖 **Bot Sosial & Chatbot** (Discord, Telegram, WhatsApp bot)
- 🌐 **Web Widget / Generator Kutipan Harian** (Daily Anime Quote)

### 🚀 Peningkatan dari Dataset Asli (Upgrade Highlights)
Dataset ini berakar dan dikembangkan dari dataset awal [quotesnime-database](https://github.com/cabrata/quotesnime-database) oleh [@cabrata](https://github.com/cabrata). Pada versi pemutakhiran ini, telah dilakukan **pembersihan kualitas data, standardisasi bahasa, serta ekspansi multibahasa besar-besaran**, antara lain:

1. ✍️ **Koreksi Tipografi & Bahasa Baku**:
   - Memperbaiki puluhan salah ketik (*typo*) seperti *bagitu* $\rightarrow$ *begitu*, *manggampangkan* $\rightarrow$ *menggampangkan*, *payang* $\rightarrow$ *payah*, *tertapi* $\rightarrow$ *tetapi*, *suksus* $\rightarrow$ *sukses*, dll.
   - Penyesuaian ke bentuk baku KBBI (misal: *merubah/rubahlah* $\rightarrow$ *mengubah/ubahlah*, *nasehat* $\rightarrow$ *nasihat*, *menggerakan* $\rightarrow$ *menggerakkan*, *berfikir* $\rightarrow$ *berpikir*).
   - Memperbaiki kalimat yang menempel tanpa spasi setelah tanda baca titik (`.`), tanda tanya (`?`), dan kurung siku (`]`).
2. 🌏 **Ekspansi Multibahasa (5 Bahasa Dunia)**:
   - Dari dataset asal yang hanya tersedia dalam 1 bahasa (Indonesia), kini diperluas secara lengkap ke dalam 5 bahasa: **Indonesia (ID)**, **Inggris (EN)**, **Jepang (JA)**, **Filipina (TL)**, dan **Malaysia (MS)** dengan total **9.605 kutipan**.
3. 🏷️ **Penyelarasan Kategori Tematik**:
   - Lebih dari 1.300+ kategori topik diterjemahkan secara rapi dan selaras ke masing-masing bahasa target tanpa merusak struktur array.
4. 📁 **Arsitektur Direktori Modern & Production-Ready**:
   - Penataan subfolder terstandarisasi per kode bahasa (`data/id/`, `data/en/`, `data/ja/`, dll.) yang rapi untuk repositori GitHub dan siap di-fetch secara instan via jsDelivr CDN.

### ✨ Keunggulan Dataset
1. **Skema Data Seragam**: Struktur kunci JSON (`character`, `quotes`, `anime`, `episode`, `category`) 100% konsisten di semua bahasa, memudahkan *switching language* secara dinamis di sisi klien.
2. **Relasi Entitas Konsisten**: Nama karakter dan judul anime tetap menggunakan penamaan baku Romaji di seluruh versi bahasa agar memudahkan relasi data, pencarian (*filtering*), dan *indexing*.
3. **Kategori Tematik Terstruktur**: Dilengkapi dengan lebih dari 1.300+ kategori topik (kehidupan, cinta, persahabatan, motivasi, dll.) yang diterjemahkan sesuai bahasa masing-masing.
4. **Siap CDN (Tanpa Server Tambahan)**: Berkas data dapat diakses langsung menggunakan CDN gratis seperti jsDelivr dengan waktu *load* sangat cepat.

---

## 📂 Struktur Direktori

```text
.
├── kata-anime-indonesia.json          # File utama Bahasa Indonesia (root)
├── data/
│   ├── id/
│   │   └── kata-anime-indonesia.json   # 🇮🇩 Bahasa Indonesia (1.921 kutipan)
│   ├── en/
│   │   └── kata-anime-english.json     # 🇬🇧 English (1.921 kutipan)
│   ├── ja/
│   │   └── kata-anime-japanese.json    # 🇯🇵 Japanese / 日本語 (1.921 kutipan)
│   ├── tl/
│   │   └── kata-anime-filipino.json    # 🇵🇭 Filipino / Tagalog (1.921 kutipan)
│   └── ms/
│       └── kata-anime-malaysian.json   # 🇲🇾 Bahasa Melayu (1.921 kutipan)
├── .gitignore                         # Pengaturan ignore berkas non-dataset
└── README.md                          # Dokumentasi proyek
```

---

## 📋 Skema Data JSON

Setiap item kutipan memiliki format objek berikut:

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
| Field | Tipe Data | Deskripsi |
| :--- | :--- | :--- |
| `character` | `string` | Nama karakter penutur (menggunakan ejaan baku Romaji agar seragam antar bahasa). |
| `quotes` | `string` | Teks kutipan yang telah diterjemahkan dan disesuaikan dengan bahasa target. |
| `anime` | `string` | Judul seri anime asal kutipan (menggunakan ejaan resmi / Romaji). |
| `episode` | `number \| null` | Nomor episode kemunculan kutipan. |
| `category` | `string[]` | Label kategori tema yang diterjemahkan sesuai bahasa target. |

---

## 🌐 Contoh Penggunaan di Aplikasi / API Publik

### 1. Akses Langsung Melalui CDN GitHub (jsDelivr / Raw)
Anda dapat langsung memanggil dataset tanpa perlu setup server backend:

```javascript
// Contoh fetch dataset Bahasa Inggris via jsDelivr CDN
const url = 'https://cdn.jsdelivr.net/gh/ranggaadipermana/kata-anime@main/data/en/kata-anime-english.json';

async function getRandomQuote() {
  const response = await fetch(url);
  const data = await response.json();
  const random = data[Math.floor(Math.random() * data.length)];
  console.log(`"${random.quotes}" — ${random.character} (${random.anime})`);
}

getRandomQuote();
```

### 2. Node.js / Express API Server
Implementasi endpoint API sederhana dengan parameter bahasa:

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

// Endpoint: GET /api/quotes/random?lang=ja
app.get('/api/quotes/random', (req, res) => {
  const lang = req.query.lang || 'id';
  const data = datasets[lang] || datasets['id'];
  const randomQuote = data[Math.floor(Math.random() * data.length)];
  res.json({
    success: true,
    data: randomQuote
  });
});

app.listen(3000, () => console.log('API running on http://localhost:3000'));
```

---

## 📊 Ringkasan Statistik
- **Total Kutipan**: 1.921 entri unik per bahasa (**Total: 9.605 kutipan**)
- **Jumlah Kategori**: ~1.309 kategori unik per bahasa
- **Dukungan Bahasa**:
  - 🇮🇩 **ID** (`kata-anime-indonesia.json`)
  - 🇬🇧 **EN** (`kata-anime-english.json`)
  - 🇯🇵 **JA** (`kata-anime-japanese.json`)
  - 🇵🇭 **TL** (`kata-anime-filipino.json`)
  - 🇲🇾 **MS** (`kata-anime-malaysian.json`)

---

## 🙏 Kredit & Penghargaan (Credits & Acknowledgments)
- Terima kasih dan apresiasi sebesar-besarnya kepada [@cabrata](https://github.com/cabrata) atas inisiatif awal pengumpulan data pada repositori [quotesnime-database](https://github.com/cabrata/quotesnime-database).

---

## 🤝 Kontribusi & Lisensi
Kontribusi saran perbaikan salah ketik atau penambahan kutipan sangat diterima melalui *Pull Request* atau *Issues* di GitHub. Dataset ini bebas digunakan untuk proyek non-komersial maupun komersial dengan tetap mencantumkan atribusi repositori ini.

---

## ⚖️ Penyangkalan Hak Cipta (Disclaimer)

> [!IMPORTANT]
> **Pemberitahuan Hak Cipta & Kekayaan Intelektual:**
>
> Seluruh judul anime, nama karakter, dialog/kutipan asli, serta materi terkait yang terdapat di dalam repositori ini merupakan **hak cipta dan kekayaan intelektual sepenuhnya milik masing-masing pencipta, pengarang (*mangaka* / penulis *light novel*), studio animasi, penerbit, dan komite produksi anime yang bersangkutan**.
>
> Repositori dan dataset ini disusun semata-mata untuk **tujuan edukasi, dokumentasi, apresiasi seni budaya, dan pengembangan riset teknologi/perangkat lunak (*fair use*)**. Proyek ini bersifat independen dan tidak terafiliasi, disponsori, atau didukung secara resmi oleh pemegang hak cipta mana pun.
>
> Jika Anda adalah pemegang hak cipta sah dan berkeberatan atas pencantuman konten tertentu di dalam repositori ini, silakan ajukan permohonan peninjauan atau penghapusan melalui [GitHub Issues](https://github.com/ranggaadipermana/kata-anime/issues).

<details>
<summary><b>English Version (Copyright Disclaimer)</b></summary>

> All anime titles, character names, original dialogue/quotes, and associated materials in this repository are the **copyrighted property and intellectual property of their respective creators, authors, animation studios, publishers, and production committees**.
>
> This dataset is compiled strictly for **educational, archival, community appreciation, and non-commercial software development purposes under fair use principles**. This project is completely independent and is not affiliated with, endorsed by, or sponsored by any official copyright owners.
>
> If you are a verified copyright owner and wish to request the review or removal of any specific content, please submit a request via [GitHub Issues](https://github.com/ranggaadipermana/kata-anime/issues).

</details>
