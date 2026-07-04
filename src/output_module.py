"""
output_module.py
----------------
Exports generated notes to Markdown and PDF formats.
"""

import os
import re
from datetime import datetime
from fpdf import FPDF


def clean_text(text: str) -> str:
    replacements = {
        "\u2014": "-", "\u2013": "-", "\u2012": "-",
        "\u2018": "'", "\u2019": "'",
        "\u201c": '"', "\u201d": '"',
        "\u2022": "-", "\u2026": "...",
        "\u00e9": "e", "\u00e8": "e", "\u00ea": "e",
        "\u00e0": "a", "\u00e2": "a",
        "\u00f9": "u", "\u00fb": "u",
        "\u00ee": "i", "\u00ef": "i",
        "\u00f4": "o", "\u00e7": "c",
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    text = text.encode("ascii", errors="ignore").decode("ascii")
    return text.strip()


def save_markdown(notes: str, output_dir: str, filename: str = None) -> str:
    os.makedirs(output_dir, exist_ok=True)
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"notes_{timestamp}.md"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(notes)
    return filepath


class NotesPDF(FPDF):
    def __init__(self, title="Study Notes"):
        super().__init__()
        self.doc_title = clean_text(title)[:60]

    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(80, 80, 80)
        self.cell(0, 8, self.doc_title, align="L",
                  new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(200, 200, 200)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def write_line(self, text, font="Helvetica", style="", size=10, color=(60, 60, 60)):
        text = clean_text(text)
        if not text:
            self.ln(2)
            return
        self.set_font(font, style, size)
        self.set_text_color(*color)
        try:
            self.multi_cell(0, 6, text)
        except Exception:
            pass
        self.ln(1)


def markdown_to_pdf(notes: str, output_dir: str, title: str = "Study Notes", filename: str = None) -> str:
    os.makedirs(output_dir, exist_ok=True)
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"notes_{timestamp}.pdf"

    filepath = os.path.join(output_dir, filename)
    pdf = NotesPDF(title=title)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_margins(15, 25, 15)

    for line in notes.split("\n"):
        s = clean_text(line.strip())
        if not s:
            pdf.ln(2)
            continue

        # Remove markdown bold/italic markers
        s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
        s = re.sub(r"\*(.+?)\*", r"\1", s)

        try:
            if s.startswith("# "):
                pdf.write_line(s[2:], style="B", size=16, color=(20, 20, 20))
                pdf.ln(1)

            elif s.startswith("## "):
                pdf.ln(2)
                pdf.write_line(s[3:], style="B", size=13, color=(30, 80, 160))

            elif s.startswith("### "):
                pdf.ln(1)
                pdf.write_line(s[4:], style="B", size=11, color=(50, 50, 50))

            elif s.startswith("- ") or s.startswith("* "):
                pdf.write_line("  -  " + s[2:], size=10, color=(60, 60, 60))

            elif s.startswith("|"):
                if "---" in s:
                    continue
                cells = [c.strip()
                         for c in s.strip("|").split("|") if c.strip()]
                row_text = "  |  ".join(cells)
                if row_text:
                    pdf.write_line(row_text, size=10, color=(60, 60, 60))

            elif s.startswith("```"):
                continue

            elif s == "---":
                pdf.set_draw_color(200, 200, 200)
                pdf.line(15, pdf.get_y(), 195, pdf.get_y())
                pdf.ln(4)

            else:
                pdf.write_line(s, size=10, color=(60, 60, 60))

        except Exception:
            continue

    pdf.output(filepath)
    return filepath
