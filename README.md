# webm2webp

Tool kecil berbasis Python untuk mengonversi file `.webm` menjadi animasi `.webp`.

![Preview GUI](docs/gui-preview.png)

Project ini mendukung:
- konversi satu atau banyak file sekaligus
- drag & drop banyak file di GUI
- pengaturan `FPS`, `Quality`, dan lebar output
- build menjadi aplikasi macOS `.app`
- build menjadi installer macOS `.pkg`
- workflow GitHub Release untuk artefak macOS Intel dan Apple Silicon

Riwayat perubahan versi tersedia di [CHANGELOG.md](CHANGELOG.md).
Bagian `Unreleased` di changelog bisa dipakai untuk mencatat perubahan sebelum membuat tag release berikutnya.
Panduan release langkah demi langkah tersedia di [RELEASE.md](RELEASE.md).
Panduan kontribusi tersedia di [CONTRIBUTING.md](CONTRIBUTING.md).
Project ini menggunakan lisensi [MIT](LICENSE).

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

Preview GUI di README ini digenerate dari aplikasi langsung dengan:

```bash
QT_QPA_PLATFORM=offscreen ./venv/bin/python scripts/render_gui_preview.py docs/gui-preview.png
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

Script build akan:
- membuat icon app otomatis
- mengubah icon ke format `.icns`
- membangun `WebM2WebP.app` dengan PyInstaller

Untuk signing app opsional:

```bash
APP_SIGN_IDENTITY="Developer ID Application: Nama Anda (TEAMID)" ./build_macos_app.sh
```

## Build Installer macOS

```bash
./build_macos_pkg.sh
```

Atau dengan versi package eksplisit:

```bash
./build_macos_pkg.sh 1.0.3
```

Hasil build akan tersedia di:

```bash
dist/WebM2WebP.pkg
```

Script installer akan:
- memastikan `WebM2WebP.app` sudah ter-build
- membuat installer `.pkg` yang menginstal app ke `/Applications`
- memakai versi dari argumen, `VERSION`, atau tag git terbaru bila tersedia
- menandatangani installer jika `PKG_SIGN_IDENTITY` disediakan

Contoh signing installer:

```bash
PKG_SIGN_IDENTITY="Developer ID Installer: Nama Anda (TEAMID)" ./build_macos_pkg.sh 1.0.3
```

Jika Anda ingin distribusi yang lebih mulus di macOS, biasanya app dan package sama-sama ditandatangani:

```bash
APP_SIGN_IDENTITY="Developer ID Application: Nama Anda (TEAMID)" \
PKG_SIGN_IDENTITY="Developer ID Installer: Nama Anda (TEAMID)" \
./build_macos_pkg.sh 1.0.3
```

Untuk notarization opsional, Anda bisa memakai profil keychain `notarytool`:

```bash
APP_SIGN_IDENTITY="Developer ID Application: Nama Anda (TEAMID)" \
PKG_SIGN_IDENTITY="Developer ID Installer: Nama Anda (TEAMID)" \
NOTARY_KEYCHAIN_PROFILE="AC_NOTARY" \
./build_macos_pkg.sh 1.0.3
```

Atau langsung lewat kredensial environment variable:

```bash
APP_SIGN_IDENTITY="Developer ID Application: Nama Anda (TEAMID)" \
PKG_SIGN_IDENTITY="Developer ID Installer: Nama Anda (TEAMID)" \
NOTARY_APPLE_ID="nama@contoh.com" \
NOTARY_TEAM_ID="TEAMID" \
NOTARY_PASSWORD="app-specific-password" \
./build_macos_pkg.sh 1.0.3
```

## Release Artefak dari GitHub

Repository ini sudah disiapkan dengan GitHub Actions untuk build artefak macOS otomatis saat Anda push tag versi.

Contoh:

```bash
git tag v1.0.0
git push origin v1.0.0
```

Setelah itu workflow GitHub akan:
- build `WebM2WebP.app`
- zip hasil build menjadi `WebM2WebP-macos-x86_64.zip` dan `WebM2WebP-macos-arm64.zip`
- build installer menjadi `WebM2WebP-macos-x86_64.pkg` dan `WebM2WebP-macos-arm64.pkg`
- upload semua artefak ke GitHub Release dengan tag yang sama

Jika Anda ingin GitHub Actions menghasilkan artefak signed atau notarized, siapkan secrets berikut:
- `APPLE_CERTIFICATE_P12_BASE64` untuk file sertifikat `.p12` yang sudah di-encode base64
- `APPLE_CERTIFICATE_PASSWORD` untuk password file `.p12`
- `KEYCHAIN_PASSWORD` untuk keychain sementara di runner
- `APP_SIGN_IDENTITY` misalnya `Developer ID Application: Nama Anda (TEAMID)`
- `PKG_SIGN_IDENTITY` misalnya `Developer ID Installer: Nama Anda (TEAMID)`
- `NOTARY_APPLE_ID`, `NOTARY_TEAM_ID`, dan `NOTARY_PASSWORD` untuk notarization berbasis Apple ID

Contoh membuat nilai base64 di macOS:

```bash
base64 -i developer-id.p12 | pbcopy
```

## Catatan

- Output `.webp` akan dibuat di folder yang sama dengan file input.
- Temporary frame disimpan di folder sementara agar aman untuk batch convert.
- App akan mencoba mencari `ffmpeg` dan `img2webp` di `PATH`, `/usr/local/bin`, dan `/opt/homebrew/bin`. Ini penting saat app dibuka dari Finder di macOS.
- Artefak build lebih aman disimpan di GitHub Releases daripada commit hasil build langsung ke repository.
- Build default tetap unsigned. Untuk distribusi publik, sebaiknya gunakan `APP_SIGN_IDENTITY`, `PKG_SIGN_IDENTITY`, dan salah satu set kredensial notarization.
