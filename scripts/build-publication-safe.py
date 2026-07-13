#!/usr/bin/env python3
from __future__ import annotations

import base64
import importlib.util
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = ROOT / "scripts/build-publication.py"


def load_builder():
    spec = importlib.util.spec_from_file_location("kvas_publication_builder", ORIGINAL)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {ORIGINAL}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def find_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def generated_card(path: Path) -> None:
    width, height = 1200, 630
    image = Image.new("RGB", (width, height), (26, 18, 11))
    pixels = image.load()
    for y in range(height):
        for x in range(width):
            glow = max(0.0, 1.0 - ((x - 920) ** 2 + (y - 145) ** 2) ** 0.5 / 850)
            pixels[x, y] = (
                int(26 + 58 * glow),
                int(18 + 38 * glow),
                int(11 + 17 * glow),
            )

    draw = ImageDraw.Draw(image)
    title = find_font(92)
    subtitle = find_font(46)
    small = find_font(30)

    draw.rounded_rectangle((55, 55, 1145, 575), radius=34, fill=(32, 24, 15), outline=(238, 181, 63), width=3)
    draw.text((95, 105), "КВАС", font=title, fill=(255, 250, 237))
    draw.text((95, 210), "ЖИЖА", font=title, fill=(238, 181, 63))
    draw.text((95, 335), "для ИИ-агента", font=subtitle, fill=(255, 250, 237))
    draw.text((95, 430), "PDF + WEB  ·  RU  EN  ES  DE  ZH-CN", font=small, fill=(215, 199, 174))
    draw.text((95, 495), "Версия 1.1.0", font=small, fill=(238, 181, 63))

    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, format="JPEG", quality=90, optimize=True, progressive=True)


def safe_build_share_image(root: Path, site: Path) -> None:
    output = site / "assets/kvas-zhizha-ai-agent-1.1.0.jpg"
    parts = sorted((root / "share/assets").glob("card-1.0.4.b64.part*"))

    if parts:
        try:
            encoded = "".join(part.read_text(encoding="utf-8") for part in parts)
            encoded = re.sub(r"\s+", "", encoded)
            encoded += "=" * (-len(encoded) % 4)
            data = base64.b64decode(encoded, validate=False)
            if data.startswith(b"\xff\xd8") and data.endswith(b"\xff\xd9"):
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_bytes(data)
                print(f"Recovered Telegram JPEG from {len(parts)} Base64 chunks")
                return
            print("Warning: recovered share-card data is not a complete JPEG; generating fallback")
        except Exception as exc:
            print(f"Warning: cannot recover share-card chunks ({exc}); generating fallback")

    generated_card(output)
    print(f"Generated fallback Telegram card: {output}")


def main() -> None:
    builder = load_builder()
    builder.build_share_image = safe_build_share_image
    builder.main()


if __name__ == "__main__":
    main()
