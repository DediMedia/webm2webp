import argparse
import subprocess
import tempfile
from pathlib import Path


def webm_to_webp(input_file, output_file=None, fps=10, scale=800, quality=75):
    input_path = Path(input_file).expanduser().resolve()
    output_path = Path(output_file).expanduser().resolve() if output_file else input_path.with_suffix(".webp")

    with tempfile.TemporaryDirectory(prefix="webm2webp_") as temp_dir:
        frame_pattern = str(Path(temp_dir) / "frame_%04d.png")

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(input_path),
                "-vf",
                f"fps={fps},scale={scale}:-1",
                frame_pattern,
            ],
            check=True,
        )

        frames = sorted(str(path) for path in Path(temp_dir).glob("frame_*.png"))
        if not frames:
            raise RuntimeError(f"Tidak ada frame yang berhasil diekstrak dari {input_path.name}")

        subprocess.run(
            [
                "img2webp",
                "-loop",
                "0",
                "-q",
                str(quality),
                *frames,
                "-o",
                str(output_path),
            ],
            check=True,
        )

    return output_path


def convert_many(input_files, fps=10, scale=800, quality=75, progress_callback=None):
    results = []

    for index, input_file in enumerate(input_files, start=1):
        input_path = Path(input_file).expanduser().resolve()
        output_path = webm_to_webp(
            input_path,
            fps=fps,
            scale=scale,
            quality=quality,
        )
        results.append(output_path)

        if progress_callback is not None:
            progress_callback(index, len(input_files), input_path, output_path)

    return results


def parse_args():
    parser = argparse.ArgumentParser(description="Konversi file WEBM menjadi WEBP animasi.")
    parser.add_argument("inputs", nargs="+", help="Satu atau lebih file .webm")
    parser.add_argument("--fps", type=int, default=10, help="FPS output")
    parser.add_argument("--scale", type=int, default=800, help="Lebar output, tinggi otomatis")
    parser.add_argument("--quality", type=int, default=75, help="Kualitas WEBP")
    return parser.parse_args()


def main():
    args = parse_args()

    for output_path in convert_many(
        args.inputs,
        fps=args.fps,
        scale=args.scale,
        quality=args.quality,
    ):
        print(f"Berhasil: {output_path}")


if __name__ == "__main__":
    main()
