#!/bin/zsh

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON_BIN="${ROOT_DIR}/venv/bin/python"
ICON_PNG="${ROOT_DIR}/assets/icon_1024.png"
ICON_ICNS="${ROOT_DIR}/assets/WebM2WebP.icns"
ICONSET_DIR="${ROOT_DIR}/assets/WebM2WebP.iconset"

if [[ ! -x "${PYTHON_BIN}" ]]; then
  echo "Virtualenv tidak ditemukan di ${PYTHON_BIN}"
  echo "Buat virtualenv dulu, lalu install dependency dari requirements.txt"
  exit 1
fi

if ! "${PYTHON_BIN}" -m PyInstaller --version >/dev/null 2>&1; then
  echo "PyInstaller belum terpasang."
  echo "Jalankan: ${PYTHON_BIN} -m pip install -r ${ROOT_DIR}/requirements.txt"
  exit 1
fi

cd "${ROOT_DIR}"

mkdir -p "${ROOT_DIR}/assets"

if [[ ! -f "${ICON_PNG}" ]]; then
  echo "Membuat icon PNG..."
  "${PYTHON_BIN}" "${ROOT_DIR}/scripts/generate_app_icon.py" "${ICON_PNG}"
fi

if [[ ! -f "${ICON_ICNS}" ]]; then
  echo "Membuat icon ICNS..."
  rm -rf "${ICONSET_DIR}" "${ICON_ICNS}"
  mkdir -p "${ICONSET_DIR}"

  cp "${ICON_PNG}" "${ICONSET_DIR}/icon_512x512@2x.png"
  sips -z 16 16 "${ICON_PNG}" --out "${ICONSET_DIR}/icon_16x16.png" >/dev/null
  sips -z 32 32 "${ICON_PNG}" --out "${ICONSET_DIR}/icon_16x16@2x.png" >/dev/null
  sips -z 32 32 "${ICON_PNG}" --out "${ICONSET_DIR}/icon_32x32.png" >/dev/null
  sips -z 64 64 "${ICON_PNG}" --out "${ICONSET_DIR}/icon_32x32@2x.png" >/dev/null
  sips -z 128 128 "${ICON_PNG}" --out "${ICONSET_DIR}/icon_128x128.png" >/dev/null
  sips -z 256 256 "${ICON_PNG}" --out "${ICONSET_DIR}/icon_128x128@2x.png" >/dev/null
  sips -z 256 256 "${ICON_PNG}" --out "${ICONSET_DIR}/icon_256x256.png" >/dev/null
  sips -z 512 512 "${ICON_PNG}" --out "${ICONSET_DIR}/icon_256x256@2x.png" >/dev/null
  sips -z 512 512 "${ICON_PNG}" --out "${ICONSET_DIR}/icon_512x512.png" >/dev/null
  iconutil -c icns "${ICONSET_DIR}" -o "${ICON_ICNS}"
  rm -rf "${ICONSET_DIR}"
else
  echo "Menggunakan icon ICNS yang sudah ada: ${ICON_ICNS}"
fi

rm -rf build dist WebM2WebP.spec

"${PYTHON_BIN}" -m PyInstaller \
  --noconfirm \
  --windowed \
  --name "WebM2WebP" \
  --icon "${ICON_ICNS}" \
  webm2webp_gui.py

echo "Build selesai."
echo "App: ${ROOT_DIR}/dist/WebM2WebP.app"
echo "Pastikan ffmpeg dan img2webp tersedia di PATH saat app dijalankan."
