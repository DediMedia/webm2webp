#!/bin/zsh

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
APP_BUNDLE="${ROOT_DIR}/dist/WebM2WebP.app"
PKG_ID="com.dedimedia.webm2webp"
VERSION_INPUT="${1:-${VERSION:-}}"
PKG_SIGN_IDENTITY="${PKG_SIGN_IDENTITY:-}"
NOTARY_KEYCHAIN_PROFILE="${NOTARY_KEYCHAIN_PROFILE:-}"
NOTARY_APPLE_ID="${NOTARY_APPLE_ID:-}"
NOTARY_TEAM_ID="${NOTARY_TEAM_ID:-}"
NOTARY_PASSWORD="${NOTARY_PASSWORD:-}"

detect_version() {
  local version

  if [[ -n "${VERSION_INPUT}" ]]; then
    echo "${VERSION_INPUT}"
    return
  fi

  if command -v git >/dev/null 2>&1; then
    version="$(git -C "${ROOT_DIR}" describe --tags --abbrev=0 2>/dev/null || true)"
    version="${version#v}"
    if [[ -n "${version}" ]]; then
      echo "${version}"
      return
    fi
  fi

  echo "1.0.0"
}

VERSION="$(detect_version)"
PKG_PATH="${ROOT_DIR}/dist/WebM2WebP.pkg"
UNSIGNED_PKG_PATH="${ROOT_DIR}/dist/WebM2WebP-unsigned.pkg"

run_notarization() {
  if [[ -z "${NOTARY_KEYCHAIN_PROFILE}" && ( -z "${NOTARY_APPLE_ID}" || -z "${NOTARY_TEAM_ID}" || -z "${NOTARY_PASSWORD}" ) ]]; then
    return
  fi

  if ! command -v xcrun >/dev/null 2>&1; then
    echo "xcrun tidak tersedia."
    echo "Notarization membutuhkan Xcode Command Line Tools."
    exit 1
  fi

  echo "Mengirim package ke notary service Apple..."

  if [[ -n "${NOTARY_KEYCHAIN_PROFILE}" ]]; then
    xcrun notarytool submit "${PKG_PATH}" \
      --keychain-profile "${NOTARY_KEYCHAIN_PROFILE}" \
      --wait
  elif [[ -n "${NOTARY_APPLE_ID}" && -n "${NOTARY_TEAM_ID}" && -n "${NOTARY_PASSWORD}" ]]; then
    xcrun notarytool submit "${PKG_PATH}" \
      --apple-id "${NOTARY_APPLE_ID}" \
      --team-id "${NOTARY_TEAM_ID}" \
      --password "${NOTARY_PASSWORD}" \
      --wait
  else
    return
  fi

  echo "Menjalankan stapler pada package..."
  xcrun stapler staple "${PKG_PATH}"
  echo "Memverifikasi hasil stapler..."
  xcrun stapler validate "${PKG_PATH}"
}

if ! command -v pkgbuild >/dev/null 2>&1; then
  echo "pkgbuild tidak tersedia."
  echo "Script ini harus dijalankan di macOS."
  exit 1
fi

if [[ ! -d "${APP_BUNDLE}" ]]; then
  echo "App bundle belum ada di ${APP_BUNDLE}"
  echo "Menjalankan build_macos_app.sh terlebih dahulu..."
  "${ROOT_DIR}/build_macos_app.sh"
fi

rm -f "${PKG_PATH}" "${UNSIGNED_PKG_PATH}"

pkgbuild \
  --component "${APP_BUNDLE}" \
  --install-location /Applications \
  --identifier "${PKG_ID}" \
  --version "${VERSION}" \
  "${UNSIGNED_PKG_PATH}"

if [[ -n "${PKG_SIGN_IDENTITY}" ]]; then
  if ! command -v productsign >/dev/null 2>&1; then
    echo "productsign tidak tersedia."
    echo "Signing package membutuhkan tools bawaan macOS."
    exit 1
  fi

  echo "Signing installer dengan identity: ${PKG_SIGN_IDENTITY}"
  productsign \
    --sign "${PKG_SIGN_IDENTITY}" \
    "${UNSIGNED_PKG_PATH}" \
    "${PKG_PATH}"
  rm -f "${UNSIGNED_PKG_PATH}"
else
  mv "${UNSIGNED_PKG_PATH}" "${PKG_PATH}"
fi

run_notarization

echo "Build installer selesai."
echo "Package: ${PKG_PATH}"
echo "Version: ${VERSION}"
