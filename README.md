# webm2webp

Tool kecil berbasis Python untuk mengonversi file `.webm` menjadi animasi `.webp`.

Project ini mendukung:
- konversi satu atau banyak file sekaligus
- drag & drop banyak file di GUI
- pengaturan `FPS`, `Quality`, dan lebar output
- build menjadi aplikasi macOS `.app`

## Kebutuhan

Pastikan tools berikut tersedia:

- `ffmpeg`
- `img2webp`
- Python 3

Contoh install di macOS dengan Homebrew:

```bash
brew install ffmpeg webp
```

## Install

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Menjalankan GUI

```bash
python3 webm2webp_gui.py
```

Fitur GUI:
- pilih banyak file `.webm`
- drag & drop banyak file langsung ke jendela
- progress bar saat proses konversi
- pengaturan `FPS`, `Lebar`, dan `Quality`

## Menjalankan via CLI

```bash
python3 webm2webp.py file1.webm file2.webm
```

Contoh dengan pengaturan custom:

```bash
python3 webm2webp.py input.webm --fps 12 --scale 720 --quality 80
```

## Build App macOS

```bash
./build_macos_app.sh
```

Hasil build akan tersedia di:

```bash
dist/WebM2WebP.app
```

## Catatan

- Output `.webp` akan dibuat di folder yang sama dengan file input.
- Temporary frame disimpan di folder sementara agar aman untuk batch convert.
- Jika ke depan ingin menyimpan artefak build, lebih aman memakai GitHub Releases daripada commit hasil build langsung ke repository.
