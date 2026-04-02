import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def _bundle_bin_dirs():
    executable_path = Path(sys.executable).resolve()
    candidates = []

    # PyInstaller app bundle on macOS keeps resources under Contents/Resources.
    candidates.append(executable_path.parent.parent / "Resources" / "bin")

    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        candidates.append(Path(meipass) / "bin")

    return [path for path in candidates if path.exists()]


def resolve_command(command_name):
    env_key = f"WEBM2WEBP_{command_name.upper()}"
    env_path = os.environ.get(env_key)
    if env_path:
        candidate = Path(env_path).expanduser()
        if candidate.exists():
            return str(candidate.resolve())

    direct_match = shutil.which(command_name)
    if direct_match:
        return direct_match

    for bin_dir in _bundle_bin_dirs():
        candidate = bin_dir / command_name
        if candidate.exists():
            return str(candidate)

    common_bin_dirs = [
        Path("/opt/homebrew/bin"),
        Path("/usr/local/bin"),
        Path("/opt/local/bin"),
        Path.home() / ".local" / "bin",
    ]
    for bin_dir in common_bin_dirs:
        candidate = bin_dir / command_name
        if candidate.exists():
            return str(candidate)

    searched_paths = [str(path) for path in _bundle_bin_dirs()]
    searched_paths.extend(str(path) for path in common_bin_dirs)
    raise RuntimeError(
        f"'{command_name}' tidak ditemukan. Install tool ini lalu coba lagi. "
        f"Lokasi yang dicek: PATH, {', '.join(searched_paths)}. "
        f"Anda juga bisa set environment variable {env_key}."
    )


def webm_to_webp(input_file, output_file=None, fps=10, scale=800, quality=75):
    input_path = Path(input_file).expanduser().resolve()
    output_path = Path(output_file).expanduser().resolve() if output_file else input_path.with_suffix(".webp")
    ffmpeg_bin = resolve_command("ffmpeg")
    img2webp_bin = resolve_command("img2webp")

    with tempfile.TemporaryDirectory(prefix="webm2webp_") as temp_dir:
        frame_pattern = str(Path(temp_dir) / "frame_%04d.png")

        subprocess.run(
            [
                ffmpeg_bin,
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
                img2webp_bin,
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
