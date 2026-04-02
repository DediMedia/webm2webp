#!/bin/zsh

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON_BIN="${ROOT_DIR}/venv/bin/python"

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

rm -rf build dist WebM2WebP.spec

"${PYTHON_BIN}" -m PyInstaller \
  --noconfirm \
  --windowed \
  --name "WebM2WebP" \
  webm2webp_gui.py

echo "Build selesai."
echo "App: ${ROOT_DIR}/dist/WebM2WebP.app"
echo "Pastikan ffmpeg dan img2webp tersedia di PATH saat app dijalankan."
