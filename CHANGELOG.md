# Changelog

Semua perubahan penting pada project ini akan dicatat di file ini.

Format yang dipakai sederhana:
- versi
- tanggal rilis
- perubahan utama

## [Unreleased]

### Added
- Menambahkan script build installer macOS `.pkg` dari hasil `WebM2WebP.app`.

### Changed
- Workflow release GitHub sekarang mengupload artefak `.pkg` selain `.zip` untuk Intel dan Apple Silicon.
- README dan panduan release diperbarui agar mencakup alur build dan distribusi `.pkg`.
- Script build macOS sekarang mendukung signing opsional untuk `.app` dan `.pkg` via environment variable.
- Script build installer macOS sekarang mendukung notarization opsional via `notarytool`.
- Workflow GitHub Release sekarang mendukung import sertifikat signing dan kredensial notarization dari GitHub secrets.

### Fixed
- Belum ada perubahan tercatat.

## [1.0.2] - 2026-04-02

### Changed
- Menyesuaikan layout GUI agar label `FPS`, `Lebar`, dan `Quality` rata kiri dan progress bar lebih menonjol.
- Memperbarui preview GUI di README agar sesuai dengan tampilan aplikasi terbaru.
- Menyesuaikan workflow release GitHub agar menghasilkan artefak macOS terpisah untuk Intel (`x86_64`) dan Apple Silicon (`arm64`).

### Fixed
- Membuat app lebih andal menemukan `ffmpeg` dan `img2webp` saat dijalankan dari Finder atau hasil build `dist`.
- Menstabilkan script build macOS agar memakai icon `.icns` yang sudah ada dan tidak mudah gagal saat build lokal.

## [1.0.1] - 2026-04-02

### Changed
- Memperbarui workflow GitHub Actions release ke `actions/checkout@v6`.
- Memperbarui workflow GitHub Actions release ke `actions/setup-python@v6`.

### Fixed
- Menghilangkan warning deprecasi Node.js 20 pada proses release GitHub Actions.

## [1.0.0] - 2026-04-02

### Added
- Konversi batch `.webm` ke animasi `.webp` via CLI.
- GUI PyQt6 dengan multi-file selection dan drag & drop.
- Progress bar dan pengaturan `FPS`, `Lebar`, dan `Quality`.
- Build app macOS `.app` dengan PyInstaller.
- Ikon aplikasi dan pipeline pembentukan `.icns`.
- Workflow GitHub Release untuk build artefak macOS otomatis.
- Screenshot preview GUI di README.

### Changed
- Refactor converter agar aman untuk batch dengan temporary directory per file.
- README diperluas dengan panduan install, build, release, dan preview GUI.

### Fixed
- Membersihkan file artefak build dan cache yang sebelumnya sempat ikut ter-track di git.
