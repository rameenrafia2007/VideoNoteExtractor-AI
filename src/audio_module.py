"""
audio_module.py
---------------
Downloads audio from video URL and transcribes using OpenAI Whisper.
"""

import os
import tempfile
import yt_dlp
import whisper


def download_audio(video_url: str, output_dir: str) -> str:
    """Download audio from a video URL using yt-dlp."""
    audio_path = os.path.join(output_dir, "audio.mp3")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(output_dir, "audio.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
        "no_warnings": True,
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        },
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    # Find the downloaded audio file
    for f in os.listdir(output_dir):
        if f.startswith("audio") and f.endswith(".mp3"):
            return os.path.join(output_dir, f)

    return audio_path


def transcribe_audio(audio_path: str, model_size: str = "base") -> dict:
    """
    Transcribe audio using OpenAI Whisper.
    Returns dict with 'text' and 'segments' (with timestamps).
    """
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path, verbose=False)

    segments = []
    for seg in result.get("segments", []):
        segments.append(
            {
                "start": round(seg["start"], 2),
                "end": round(seg["end"], 2),
                "text": seg["text"].strip(),
            }
        )

    return {
        "full_text": result["text"].strip(),
        "segments": segments,
        "language": result.get("language", "en"),
    }


def format_transcript_with_timestamps(segments: list) -> str:
    """Format transcript segments with readable timestamps."""
    lines = []
    for seg in segments:
        start_min = int(seg["start"]) // 60
        start_sec = int(seg["start"]) % 60
        lines.append(f"[{start_min:02d}:{start_sec:02d}] {seg['text']}")
    return "\n".join(lines)
