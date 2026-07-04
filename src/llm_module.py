"""
llm_module.py
-------------
Fuses audio transcript + visual OCR data using Groq API
(LLaMA 3.3 70B) to generate well-structured notes.
"""

import os
from groq import Groq


def get_groq_client() -> Groq:
    """Initialize Groq client from environment variable."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not found. Please set it in your .env file."
        )
    return Groq(api_key=api_key)


def build_fusion_prompt(
    transcript: str,
    visual_content: str,
    video_title: str = "Video",
) -> str:
    """Build the prompt for multimodal note generation."""
    return f"""You are an expert academic note-taker. You have been given:
1. A full transcript of a video lecture/tutorial (with timestamps)
2. Text extracted from slides and visual frames (with timestamps)

Your task is to generate comprehensive, well-structured study notes in Markdown format.

VIDEO TITLE: {video_title}

---
TRANSCRIPT (Audio):
{transcript[:6000]}

---
VISUAL CONTENT (Slides & Frames OCR):
{visual_content[:3000]}

---

Generate detailed study notes following this EXACT structure:

# {video_title} — Study Notes

## Overview
(2-3 sentence summary of what this video covers)

## Key Concepts
(List the main topics covered, each as a bold heading with explanation)

## Detailed Notes

### [Topic 1 Title]
- Main points as bullet points
- Sub-points indented where needed
- Include any formulas, definitions, or key terms in **bold**

### [Topic 2 Title]
(repeat as needed for each major topic)

## Important Definitions & Terms
| Term | Definition |
|------|-----------|
| term | definition |

## Key Takeaways
- 3-5 most important points from the entire video

## Visual Summary
(Describe any important diagrams, charts, or visuals mentioned)

---
Rules:
- Use the timestamps to correlate audio and visual content
- Prioritize slide content for headings and structure
- Use transcript for detailed explanations
- Keep notes clear, concise, and academically rigorous
- Format all code snippets in ```code blocks```
"""


def generate_notes(
    transcript: str,
    visual_content: str,
    video_title: str = "Video",
    model: str = "llama-3.3-70b-versatile",
) -> str:
    """
    Send multimodal content to Groq LLM and get structured notes.
    """
    client = get_groq_client()
    prompt = build_fusion_prompt(transcript, visual_content, video_title)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert academic assistant specialised in "
                    "creating clear, structured, and comprehensive study notes "
                    "from video lectures. Always produce well-formatted Markdown."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=4096,
    )

    return response.choices[0].message.content


def get_video_title(video_url: str) -> str:
    """Extract video title using yt-dlp."""
    try:
        import yt_dlp

        ydl_opts = {"quiet": True, "no_warnings": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return info.get("title", "Video Notes")
    except Exception:
        return "Video Notes"
