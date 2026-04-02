import sys
from pathlib import Path

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from webm2webp_gui import App


def render_preview(output_file):
    app = QApplication([])
    window = App()
    window.resize(820, 620)
    window.set_input_files(
        [
            "/tmp/sample_intro.webm",
            "/tmp/product-demo.webm",
            "/tmp/banner-loop.webm",
        ]
    )
    window.fps_input.setValue(12)
    window.scale_input.setValue(720)
    window.quality_input.setValue(82)
    window.progress.setValue(66)
    window.status.setText("Contoh preview: 2/3 file selesai diproses")
    window.show()

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    def save_and_exit():
        window.grab().save(str(output_path))
        app.quit()

    QTimer.singleShot(150, save_and_exit)
    app.exec()


def main():
    output_file = sys.argv[1] if len(sys.argv) > 1 else "docs/gui-preview.png"
    render_preview(output_file)


if __name__ == "__main__":
    main()
