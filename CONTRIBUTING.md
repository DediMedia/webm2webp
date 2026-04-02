# Contributing

Terima kasih sudah ingin membantu project `webm2webp`.

Dokumen ini dibuat supaya kontribusi tetap sederhana, rapi, dan mudah ditinjau.

## Cara Mulai

1. Fork atau clone repository.
2. Buat virtual environment.
3. Install dependency.
4. Jalankan aplikasi atau script yang relevan.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Area Kontribusi yang Cocok

- perbaikan bug pada konversi `.webm` ke `.webp`
- peningkatan GUI PyQt6
- peningkatan build `.app` macOS
- dokumentasi
- workflow release

## Pedoman Perubahan

- Buat perubahan sekecil dan sejelas mungkin.
- Jangan commit `venv/`, `build/`, `dist/`, atau file cache.
- Jika menambah fitur, update `README.md` bila perlu.
- Jika perubahan penting, catat di `CHANGELOG.md` bagian `Unreleased`.

## Pedoman Commit

Gunakan pesan commit singkat dan jelas, misalnya:

- `Fix batch conversion error`
- `Improve GUI status message`
- `Update release workflow`

## Sebelum Membuka Pull Request

Pastikan:

- `git status` bersih dari file yang tidak sengaja ikut
- script masih bisa dijalankan
- changelog diperbarui jika perubahan memengaruhi pengguna

## Pull Request

Saat membuka PR, usahakan menjelaskan:

- apa yang berubah
- kenapa perubahan itu diperlukan
- bagaimana cara mengetesnya

## Bug Report dan Feature Request

Jika tidak ingin langsung mengirim PR, silakan gunakan issue template yang tersedia di folder `.github/ISSUE_TEMPLATE`.
