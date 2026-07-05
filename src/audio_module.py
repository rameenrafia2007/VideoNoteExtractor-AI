"""
audio_module.py
---------------
Fetches YouTube transcript - works locally and on cloud!
"""

from youtube_transcript_api import YouTubeTranscriptApi
import re


def get_video_id(url: str) -> str:
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


def download_audio(video_url: str, output_dir: str) -> str:
    return video_url


def transcribe_audio(audio_path: str, model_size: str = "base") -> dict:
    video_id = get_video_id(audio_path)
    api = YouTubeTranscriptApi()

    try:
        try:
            fetched = api.fetch(video_id, languages=['en'])
        except Exception:
            transcript_list = api.list(video_id)
            lang_code = None
            for t in transcript_list:
                lang_code = t.language_code
                break
            fetched = api.fetch(video_id, languages=[lang_code])

        segments = []
        full_text_parts = []

        for item in fetched:
            # New API returns objects, not dicts
            if hasattr(item, 'text'):
                text = item.text.strip()
                start = round(item.start, 2)
                duration = getattr(item, 'duration', 0)
            else:
                text = item.get("text", "").strip()
                start = round(item.get("start", 0), 2)
                duration = item.get("duration", 0)

            segments.append({
                "start": start,
                "end": round(start + duration, 2),
                "text": text,
            })
            full_text_parts.append(text)

        return {
            "full_text": " ".join(full_text_parts),
            "segments": segments,
            "language": "en",
        }

    except Exception as e:
        raise RuntimeError(f"Transcript fetch failed: {str(e)}")


def format_transcript_with_timestamps(segments: list) -> str:
    lines = []
    for seg in segments:
        start_min = int(seg["start"]) // 60
        start_sec = int(seg["start"]) % 60
        lines.append(f"[{start_min:02d}:{start_sec:02d}] {seg['text']}")
    return "\n".join(lines)
