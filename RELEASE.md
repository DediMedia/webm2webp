# Release Guide

Panduan singkat untuk membuat release baru `webm2webp`.

## Checklist Sebelum Release

Pastikan hal berikut sudah beres:

- perubahan baru sudah dicatat di `CHANGELOG.md` bagian `Unreleased`
- branch `main` sudah berisi commit terbaru
- working tree bersih
- aplikasi masih bisa dijalankan atau dibuild
- jika ingin release signed, sertifikat `Developer ID Application` dan `Developer ID Installer` sudah tersedia di keychain runner/lokal
- jika ingin release notarized, siapkan `NOTARY_KEYCHAIN_PROFILE` atau kombinasi `NOTARY_APPLE_ID`, `NOTARY_TEAM_ID`, dan `NOTARY_PASSWORD`
- untuk GitHub-hosted runner, sertifikat biasanya perlu diimport dari secrets `APPLE_CERTIFICATE_P12_BASE64`, `APPLE_CERTIFICATE_PASSWORD`, dan `KEYCHAIN_PASSWORD`

## 1. Cek Kondisi Repo

```bash
git status --short
git pull --ff-only origin main
```

## 2. Update Changelog

Pindahkan isi `Unreleased` ke versi baru dengan format seperti ini:

```md
## [1.0.2] - 2026-04-03
```

Lalu buat lagi section kosong:

```md
## [Unreleased]

### Added
- Belum ada perubahan tercatat.

### Changed
- Belum ada perubahan tercatat.

### Fixed
- Belum ada perubahan tercatat.
```

## 3. Commit Perubahan Release

```bash
git add CHANGELOG.md README.md
git commit -m "Prepare v1.0.2 release"
git push origin main
```

Jika hanya changelog yang berubah, cukup stage file yang relevan saja.

## 4. Buat Tag Release

```bash
git tag v1.0.2
git push origin v1.0.2
```

## 5. Tunggu GitHub Actions

Setelah tag dipush:

- workflow `Release macOS App` akan berjalan otomatis untuk dua arsitektur
- GitHub akan membuat release baru
- aset `WebM2WebP-macos-x86_64.zip` dan `WebM2WebP-macos-arm64.zip` akan diupload ke halaman Releases
- aset `WebM2WebP-macos-x86_64.pkg` dan `WebM2WebP-macos-arm64.pkg` juga akan diupload ke halaman Releases
- jika secrets signing tersedia, workflow akan import sertifikat ke keychain sementara lalu sign artefak
- jika secrets notarization tersedia, workflow akan menotarisasi file `.pkg` sebelum diupload

## 6. Verifikasi Release

Contoh pengecekan dengan GitHub CLI:

```bash
gh run list --repo DediMedia/webm2webp --limit 3
gh release view v1.0.2 --repo DediMedia/webm2webp
```

Yang perlu dicek:

- status workflow `success`
- asset `WebM2WebP-macos-x86_64.zip` tersedia untuk Intel Mac
- asset `WebM2WebP-macos-arm64.zip` tersedia untuk Apple Silicon Mac
- asset `WebM2WebP-macos-x86_64.pkg` tersedia untuk Intel Mac
- asset `WebM2WebP-macos-arm64.pkg` tersedia untuk Apple Silicon Mac
- ukuran file terlihat wajar
- release muncul di tab Releases
- jika build signed dipakai, verifikasi `pkgutil --check-signature` menunjukkan identity yang benar
- jika build notarized dipakai, verifikasi `xcrun stapler validate` berhasil pada file `.pkg`

Secrets GitHub yang relevan:

- `APPLE_CERTIFICATE_P12_BASE64`
- `APPLE_CERTIFICATE_PASSWORD`
- `KEYCHAIN_PASSWORD`
- `APP_SIGN_IDENTITY`
- `PKG_SIGN_IDENTITY`
- `NOTARY_APPLE_ID`
- `NOTARY_TEAM_ID`
- `NOTARY_PASSWORD`

## Pola Versi

Gunakan pola sederhana berikut:

- `v1.0.1` untuk perbaikan kecil
- `v1.1.0` untuk fitur baru yang masih kompatibel
- `v2.0.0` untuk perubahan besar yang memutus kompatibilitas atau mengubah alur utama
