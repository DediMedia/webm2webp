# Changelog

Semua perubahan penting pada project ini akan dicatat di file ini.

Format yang dipakai sederhana:
- versi
- tanggal rilis
- perubahan utama

## [Unreleased]

### Added
- Belum ada perubahan tercatat.

### Changed
- Belum ada perubahan tercatat.

### Fixed
- Belum ada perubahan tercatat.

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
