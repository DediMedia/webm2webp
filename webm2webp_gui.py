import sys
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QProgressBar,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from webm2webp import webm_to_webp


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WebM -> WebP Converter")
        self.setGeometry(200, 200, 520, 360)
        self.setAcceptDrops(True)

        self.input_files = []

        self.label = QLabel("Drag & drop beberapa file .webm ke sini, atau pilih manual.", self)
        self.label.setWordWrap(True)

        self.file_list = QListWidget(self)
        self.button_select = QPushButton("Pilih File")
        self.button_convert = QPushButton("Convert Semua")
        self.progress = QProgressBar(self)
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.status = QLabel("", self)
        self.status.setWordWrap(True)

        self.fps_input = QSpinBox(self)
        self.fps_input.setRange(1, 60)
        self.fps_input.setValue(10)

        self.scale_input = QSpinBox(self)
        self.scale_input.setRange(64, 4096)
        self.scale_input.setSingleStep(32)
        self.scale_input.setValue(800)

        self.quality_input = QSpinBox(self)
        self.quality_input.setRange(1, 100)
        self.quality_input.setValue(75)

        self.button_select.clicked.connect(self.select_files)
        self.button_convert.clicked.connect(self.convert)

        settings_layout = QFormLayout()
        settings_layout.addRow("FPS", self.fps_input)
        settings_layout.addRow("Lebar", self.scale_input)
        settings_layout.addRow("Quality", self.quality_input)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button_select)
        button_layout.addWidget(self.button_convert)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.file_list)
        layout.addLayout(settings_layout)
        layout.addLayout(button_layout)
        layout.addWidget(self.progress)
        layout.addWidget(self.status)
        self.setLayout(layout)

    def select_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Pilih File",
            "",
            "WEBM Files (*.webm)",
        )
        if files:
            self.set_input_files(files)

    def set_input_files(self, files):
        unique_files = []
        seen = set()
        for file in files:
            path = str(Path(file).expanduser().resolve())
            if path.lower().endswith(".webm") and path not in seen:
                seen.add(path)
                unique_files.append(path)

        self.input_files = unique_files
        self.file_list.clear()
        self.file_list.addItems([Path(file).name for file in self.input_files])

        if self.input_files:
            self.label.setText(f"{len(self.input_files)} file siap dikonversi")
            self.status.setText("")
        else:
            self.label.setText("Tidak ada file .webm yang valid")
            self.status.setText("❌ Hanya file .webm yang didukung")

    def dragEnterEvent(self, event):
        if self._has_webm_urls(event):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if self._has_webm_urls(event):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = []
        for url in event.mimeData().urls():
            local_file = url.toLocalFile()
            if local_file:
                files.append(local_file)

        self.set_input_files(files)
        event.acceptProposedAction()

    def _has_webm_urls(self, event):
        if not event.mimeData().hasUrls():
            return False

        return any(url.toLocalFile().lower().endswith(".webm") for url in event.mimeData().urls())

    def convert(self):
        if not self.input_files:
            self.status.setText("❌ Pilih atau drop file dulu")
            return

        total = len(self.input_files)
        success_count = 0
        errors = []
        fps = self.fps_input.value()
        scale = self.scale_input.value()
        quality = self.quality_input.value()

        self.button_convert.setEnabled(False)
        self.button_select.setEnabled(False)
        self.fps_input.setEnabled(False)
        self.scale_input.setEnabled(False)
        self.quality_input.setEnabled(False)
        self.progress.setValue(0)

        try:
            for index, input_file in enumerate(self.input_files, start=1):
                self.status.setText(f"Memproses {index}/{total}: {Path(input_file).name}")
                QApplication.processEvents()

                try:
                    webm_to_webp(
                        input_file,
                        fps=fps,
                        scale=scale,
                        quality=quality,
                    )
                    success_count += 1
                except Exception as exc:
                    errors.append(f"{Path(input_file).name}: {exc}")

                self.progress.setValue(int(index / total * 100))
                QApplication.processEvents()

            if errors:
                self.status.setText(
                    f"⚠️ Selesai. Berhasil {success_count}/{total}. Gagal: {' | '.join(errors)}"
                )
            else:
                self.status.setText(f"✅ Sukses. {success_count} file berhasil dikonversi")
        finally:
            self.button_convert.setEnabled(True)
            self.button_select.setEnabled(True)
            self.fps_input.setEnabled(True)
            self.scale_input.setEnabled(True)
            self.quality_input.setEnabled(True)

def main():
    app = QApplication(sys.argv)
    window = App()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
