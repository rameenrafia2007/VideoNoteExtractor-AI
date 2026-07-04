"""
vision_module.py
----------------
Extracts key frames from video and runs OCR to capture
slide text, diagrams, and on-screen visuals.
"""

import os
import cv2
import numpy as np
import pytesseract
from PIL import Image


def download_video(video_url: str, output_dir: str) -> str:
    """Download video for frame extraction using yt-dlp."""
    import yt_dlp

    video_path = os.path.join(output_dir, "video.mp4")

    ydl_opts = {
        "format": "bestvideo[height<=720]+bestaudio/best[height<=720]",
        "outtmpl": video_path,
        "quiet": True,
        "no_warnings": True,
        "merge_output_format": "mp4",
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        },
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    return video_path


def extract_key_frames(video_path: str, interval_seconds: int = 30) -> list:
    """
    Extract one frame every `interval_seconds` seconds from the video.
    Returns list of (timestamp_seconds, PIL.Image) tuples.
    """
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps if fps > 0 else 0

    frames = []
    frame_interval = int(fps * interval_seconds)

    frame_idx = 0
    while True:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if not ret:
            break

        timestamp = frame_idx / fps
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_frame)
        frames.append((round(timestamp, 1), pil_image))

        frame_idx += frame_interval
        if frame_idx >= total_frames:
            break

    cap.release()
    return frames


def is_slide_frame(image: Image.Image) -> bool:
    """
    Heuristic: detect if a frame looks like a slide/presentation
    by checking for large uniform background regions.
    """
    gray = np.array(image.convert("L"))
    std_dev = gray.std()
    return std_dev < 80  # Low variance = likely a slide


def ocr_frame(image: Image.Image) -> str:
    """Run OCR on a single frame and return extracted text."""
    # Enhance image for better OCR
    gray = image.convert("L")
    text = pytesseract.image_to_string(gray, config="--psm 6")
    return text.strip()


def extract_visual_content(frames: list, min_text_length: int = 20) -> list:
    """
    Run OCR on extracted frames, filter out frames with little/no text.
    Returns list of dicts with timestamp and extracted text.
    """
    visual_data = []
    seen_texts = set()

    for timestamp, image in frames:
        text = ocr_frame(image)

        if len(text) < min_text_length:
            continue

        # Deduplicate very similar consecutive slides
        text_key = text[:100].strip().lower()
        if text_key in seen_texts:
            continue
        seen_texts.add(text_key)

        visual_data.append(
            {
                "timestamp": timestamp,
                "text": text,
                "is_slide": is_slide_frame(image),
            }
        )

    return visual_data


def format_visual_content(visual_data: list) -> str:
    """Format visual/OCR data for LLM consumption."""
    lines = []
    for item in visual_data:
        minutes = int(item["timestamp"]) // 60
        seconds = int(item["timestamp"]) % 60
        label = "Slide" if item["is_slide"] else "Frame"
        lines.append(
            f"[{label} @ {minutes:02d}:{seconds:02d}]\n{item['text']}\n")
    return "\n".join(lines)
