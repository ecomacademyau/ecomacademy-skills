#!/usr/bin/env python3
"""Make the upload copy: same resolution, high-bitrate H.264, fast-start, saved to the brand's delivery folder.
Usage: python3 deliver.py <final.mp4> ["<clear name>"]
Delivery folder: brand.json "deliver_dir" (default <reels_home>/delivered)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common


def main():
    common.utf8_console()
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = Path(sys.argv[1]).expanduser()
    name = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] else src.stem
    brand = common.load_brand()
    out_dir = Path(brand.get("deliver_dir") or (common.reels_home() / "delivered")).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{name}.mp4"

    h = common.probe_height(src)
    rate, mx = ("35M", "45M") if h >= 3000 else ("16M", "20M")   # 4K vs 1080p
    venc = common.video_encoder(rate, mx, preset="slow")          # Apple hardware encoder on a Mac, libx264 elsewhere
    common.run([common.ffmpeg(), "-hide_banner", "-loglevel", "error", "-y", "-i", src, *venc,
                "-pix_fmt", "yuv420p", "-tag:v", "avc1", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", out])
    print(out)


if __name__ == "__main__":
    main()
