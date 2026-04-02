import binascii
import math
import struct
import sys
import zlib
from pathlib import Path


SIZE = 1024


def png_chunk(chunk_type, data):
    return (
        struct.pack(">I", len(data))
        + chunk_type
        + data
        + struct.pack(">I", binascii.crc32(chunk_type + data) & 0xFFFFFFFF)
    )


def write_png(path, width, height, rows):
    raw = bytearray()
    for row in rows:
        raw.append(0)
        raw.extend(row)

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    data = b"".join(
        [
            b"\x89PNG\r\n\x1a\n",
            png_chunk(b"IHDR", ihdr),
            png_chunk(b"IDAT", zlib.compress(bytes(raw), level=9)),
            png_chunk(b"IEND", b""),
        ]
    )
    path.write_bytes(data)


def clamp(value, low=0, high=255):
    return max(low, min(high, int(value)))


def blend(base, top):
    top_alpha = top[3] / 255.0
    base_alpha = base[3] / 255.0
    out_alpha = top_alpha + base_alpha * (1.0 - top_alpha)
    if out_alpha <= 0:
        return (0, 0, 0, 0)

    channels = []
    for index in range(3):
        out_channel = (
            top[index] * top_alpha + base[index] * base_alpha * (1.0 - top_alpha)
        ) / out_alpha
        channels.append(clamp(out_channel))

    return (*channels, clamp(out_alpha * 255))


def inside_rounded_rect(x, y, left, top, right, bottom, radius):
    if left + radius <= x <= right - radius and top <= y <= bottom:
        return True
    if left <= x <= right and top + radius <= y <= bottom - radius:
        return True

    corners = (
        (left + radius, top + radius),
        (right - radius, top + radius),
        (left + radius, bottom - radius),
        (right - radius, bottom - radius),
    )
    for cx, cy in corners:
        if (x - cx) ** 2 + (y - cy) ** 2 <= radius ** 2:
            return True
    return False


def inside_polygon(x, y, points):
    inside = False
    j = len(points) - 1
    for i in range(len(points)):
        xi, yi = points[i]
        xj, yj = points[j]
        intersects = ((yi > y) != (yj > y)) and (
            x < (xj - xi) * (y - yi) / ((yj - yi) or 1e-9) + xi
        )
        if intersects:
            inside = not inside
        j = i
    return inside


def background_color(x, y):
    vertical = y / (SIZE - 1)
    horizontal = x / (SIZE - 1)

    top = (17, 88, 111)
    bottom = (10, 31, 68)
    base = tuple(
        clamp(top[i] * (1.0 - vertical) + bottom[i] * vertical + 10 * horizontal)
        for i in range(3)
    )

    glow_x = SIZE * 0.72
    glow_y = SIZE * 0.22
    distance = math.hypot(x - glow_x, y - glow_y)
    glow = max(0.0, 1.0 - distance / 600.0)

    return (
        clamp(base[0] + 35 * glow),
        clamp(base[1] + 55 * glow),
        clamp(base[2] + 90 * glow),
        255,
    )


def render_icon():
    shadow = (0, 0, 0, 55)
    panel = (243, 248, 250, 255)
    panel_inner = (227, 237, 241, 255)
    teal = (14, 137, 150, 255)
    lime = (122, 198, 86, 255)

    left = 176
    top = 176
    right = 848
    bottom = 848
    radius = 170

    shadow_offset = 24
    arrow_left = [
        (332, 365),
        (532, 365),
        (532, 300),
        (708, 512),
        (532, 724),
        (532, 658),
        (332, 658),
        (332, 574),
        (446, 574),
        (446, 448),
        (332, 448),
    ]
    arrow_right = [
        (692, 659),
        (492, 659),
        (492, 724),
        (316, 512),
        (492, 300),
        (492, 366),
        (692, 366),
        (692, 449),
        (578, 449),
        (578, 575),
        (692, 575),
    ]

    rows = []
    for y in range(SIZE):
        row = bytearray()
        for x in range(SIZE):
            pixel = background_color(x, y)

            if inside_rounded_rect(
                x,
                y,
                left + shadow_offset,
                top + shadow_offset,
                right + shadow_offset,
                bottom + shadow_offset,
                radius,
            ):
                pixel = blend(pixel, shadow)

            if inside_rounded_rect(x, y, left, top, right, bottom, radius):
                pixel = panel

            if inside_rounded_rect(x, y, left + 30, top + 30, right - 30, bottom - 30, radius - 22):
                pixel = panel_inner

            if inside_polygon(x, y, arrow_left):
                pixel = teal

            if inside_polygon(x, y, arrow_right):
                pixel = lime

            row.extend(pixel)
        rows.append(bytes(row))
    return rows


def main():
    output_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("assets/icon_1024.png")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    write_png(output_path, SIZE, SIZE, render_icon())


if __name__ == "__main__":
    main()
