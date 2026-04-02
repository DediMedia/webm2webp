import sys
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFrame,
    QGridLayout,
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
        self.setGeometry(200, 200, 640, 430)
        self.setAcceptDrops(True)
        self.setStyleSheet(
            """
            QWidget {
                font-size: 13px;
            }
            QListWidget {
                min-height: 170px;
                padding: 8px;
            }
            QPushButton {
                min-height: 36px;
                padding: 0 16px;
            }
            QSpinBox {
                min-height: 34px;
                padding: 0 8px;
            }
            QProgressBar {
                min-height: 24px;
                border: 1px solid #cfcfcf;
                border-radius: 12px;
                background: #f4f4f4;
                text-align: center;
                font-weight: 600;
            }
            QProgressBar::chunk {
                border-radius: 12px;
                background: #3d8bfd;
            }
            """
        )

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

        settings_card = QFrame(self)
        settings_card.setFrameShape(QFrame.Shape.NoFrame)

        settings_layout = QGridLayout()
        settings_layout.setContentsMargins(0, 0, 0, 0)
        settings_layout.setHorizontalSpacing(14)
        settings_layout.setVerticalSpacing(10)

        self.fps_label = QLabel("FPS", self)
        self.scale_label = QLabel("Lebar", self)
        self.quality_label = QLabel("Quality", self)

        for row, (label, widget) in enumerate(
            [
                (self.fps_label, self.fps_input),
                (self.scale_label, self.scale_input),
                (self.quality_label, self.quality_input),
            ]
        ):
            label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            label.setMinimumWidth(64)
            settings_layout.addWidget(label, row, 0, alignment=Qt.AlignmentFlag.AlignLeft)
            settings_layout.addWidget(widget, row, 1)

        settings_layout.setColumnStretch(0, 0)
        settings_layout.setColumnStretch(1, 1)
        settings_card.setLayout(settings_layout)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        button_layout.addWidget(self.button_select)
        button_layout.addWidget(self.button_convert)
        button_layout.addStretch(1)

        layout = QVBoxLayout()
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(14)
        layout.addWidget(self.label)
        layout.addWidget(self.file_list)
        layout.addWidget(settings_card)
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
