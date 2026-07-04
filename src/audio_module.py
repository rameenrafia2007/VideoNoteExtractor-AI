"""
audio_module.py
---------------
Fetches transcript from YouTube using youtube-transcript-api v1.2+
Works perfectly on cloud!
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
        # Try English first
        try:
            fetched = api.fetch(video_id, languages=['en'])
        except Exception:
            # Try any available language
            transcript_list = api.list(video_id)
            lang_code = None
            for t in transcript_list:
                lang_code = t.language_code
                break
            if not lang_code:
                raise RuntimeError("No captions found.")
            fetched = api.fetch(video_id, languages=[lang_code])

        segments = []
        full_text_parts = []

        for item in fetched:
            text = item.get("text", "").strip()
            segments.append({
                "start": round(item.get("start", 0), 2),
                "end": round(item.get("start", 0) + item.get("duration", 0), 2),
                "text": text,
            })
            full_text_parts.append(text)

        return {
            "full_text": " ".join(full_text_parts),
            "segments": segments,
            "language": "en",
        }

    except Exception as e:
        raise RuntimeError(
            f"Transcript fetch failed: {str(e)}\n"
            "Please make sure the video has captions enabled."
        )


def format_transcript_with_timestamps(segments: list) -> str:
    lines = []
    for seg in segments:
        start_min = int(seg["start"]) // 60
        start_sec = int(seg["start"]) % 60
        lines.append(f"[{start_min:02d}:{start_sec:02d}] {seg['text']}")
    return "\n".join(lines)