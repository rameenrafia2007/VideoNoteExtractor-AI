"""
pipeline.py
-----------
Orchestrates the full video to notes pipeline.
"""

import os
import tempfile
import shutil
from src.audio_module import download_audio, transcribe_audio, format_transcript_with_timestamps
from src.vision_module import download_video, extract_key_frames, extract_visual_content, format_visual_content
from src.llm_module import generate_notes, get_video_title
from src.output_module import save_markdown, markdown_to_pdf


def run_pipeline(
    video_url: str,
    output_dir: str = "outputs",
    frame_interval: int = 30,
    whisper_model: str = "base",
    progress_callback=None,
) -> dict:

    def progress(msg, pct):
        if progress_callback:
            progress_callback(msg, pct)

    os.makedirs(output_dir, exist_ok=True)
    tmp_dir = tempfile.mkdtemp()

    try:
        progress("Fetching video info...", 5)
        title = get_video_title(video_url)
        safe_title = "".join(
            c if c.isalnum() or c in " _-" else "_" for c in title)[:50]

        progress("Downloading audio...", 15)
        audio_path = download_audio(video_url, tmp_dir)

        progress("Transcribing audio with Whisper...", 30)
        transcript_data = transcribe_audio(
            audio_path, model_size=whisper_model)
        formatted_transcript = format_transcript_with_timestamps(
            transcript_data["segments"])

        progress("Downloading video for frame analysis...", 45)
        video_path = download_video(video_url, tmp_dir)

        progress("Extracting key frames...", 55)
        frames = extract_key_frames(
            video_path, interval_seconds=frame_interval)

        progress("Running OCR on frames...", 65)
        visual_data = extract_visual_content(frames)
        formatted_visuals = format_visual_content(visual_data)

        progress("Generating notes with LLaMA 3.3 (Groq)...", 78)
        notes_markdown = generate_notes(
            transcript=formatted_transcript,
            visual_content=formatted_visuals,
            video_title=title,
        )

        progress("Saving Markdown...", 90)
        md_filename = f"{safe_title}_notes.md"
        md_path = save_markdown(
            notes_markdown, output_dir, filename=md_filename)

        progress("Generating PDF...", 95)
        pdf_filename = f"{safe_title}_notes.pdf"
        pdf_path = markdown_to_pdf(
            notes_markdown,
            output_dir,
            title=title,
            filename=pdf_filename,
        )

        progress("Done!", 100)

        return {
            "title": title,
            "markdown_path": md_path,
            "pdf_path": pdf_path,
            "notes_text": notes_markdown,
            "transcript": transcript_data["full_text"],
            "visual_frames_found": len(visual_data),
            "language": transcript_data.get("language", "en"),
        }

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
