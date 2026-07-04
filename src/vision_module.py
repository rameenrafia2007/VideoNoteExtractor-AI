"""
vision_module.py
----------------
Fetches YouTube video info and thumbnail for visual context.
No video download needed - works on cloud!
"""

import os
import urllib.request
from PIL import Image
import io


def get_video_id(url: str) -> str:
    import re
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed\/)([0-9A-Za-z_-]{11})',
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError("Invalid YouTube URL")


def download_video(video_url: str, output_dir: str) -> str:
    """Returns video URL - no download needed."""
    return video_url


def extract_key_frames(video_path: str, interval_seconds: int = 30) -> list:
    """
    Fetch YouTube thumbnails as visual frames.
    No video download needed!
    """
    video_id = get_video_id(video_path)
    frames = []

    # YouTube provides multiple thumbnails
    thumbnail_urls = [
        f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
        f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
        f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg",
    ]

    for i, thumb_url in enumerate(thumbnail_urls):
        try:
            req = urllib.request.Request(
                thumb_url,
                headers={"User-Agent": "Mozilla/5.0"}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                img_data = response.read()
                image = Image.open(io.BytesIO(img_data)).convert("RGB")
                frames.append((float(i * 30), image))
        except Exception:
            continue

    return frames


def is_slide_frame(image: Image.Image) -> bool:
    import numpy as np
    gray = np.array(image.convert("L"))
    return gray.std() < 80


def ocr_frame(image: Image.Image) -> str:
    try:
        import pytesseract
        gray = image.convert("L")
        return pytesseract.image_to_string(gray, config="--psm 6").strip()
    except Exception:
        return ""


def extract_visual_content(frames: list, min_text_length: int = 5) -> list:
    visual_data = []
    for timestamp, image in frames:
        text = ocr_frame(image)
        visual_data.append({
            "timestamp": timestamp,
            "text": text if text else "Thumbnail frame extracted",
            "is_slide": is_slide_frame(image),
        })
    return visual_data


def format_visual_content(visual_data: list) -> str:
    lines = []
    for item in visual_data:
        minutes = int(item["timestamp"]) // 60
        seconds = int(item["timestamp"]) % 60
        label = "Slide" if item["is_slide"] else "Frame"
        lines.append(
            f"[{label} @ {minutes:02d}:{seconds:02d}]\n{item['text']}\n")
    return "\n".join(lines)
