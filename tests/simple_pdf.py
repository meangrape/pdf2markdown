# -*- coding: utf-8 -*-
"""A simple PDF document generator using ReportLab."""

from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def create_simple_pdf(filename: Path = Path("simple_document.pdf")):
    doc = SimpleDocTemplate(filename.as_posix(), pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Add a title
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['h1'],
        fontSize=24,
        spaceAfter=0.25 * inch,
    )
    story.append(Paragraph("A Simple PDF Document", title_style))
    story.append(Spacer(1, 0.2 * inch)) # Add some space

    # Add a standard paragraph
    story.append(Paragraph("This is a basic paragraph in a simple PDF.", styles['Normal']))
    story.append(Spacer(1, 0.1 * inch))

    # Add another paragraph with some bold and italic text
    story.append(Paragraph("This paragraph includes <b>bold text</b> and <i>italic text</i>.", styles['Normal']))
    story.append(Spacer(1, 0.1 * inch))

    # Add a short list
    story.append(Paragraph("Here's a small list:", styles['Normal']))
    list_style = styles['Normal']
    list_style.leftIndent = 0.5 * inch
    story.append(Paragraph("• Item 1", list_style))
    story.append(Paragraph("• Item 2", list_style))

    # Build the PDF
    doc.build(story)
    print(f"Created {filename}")


if __name__ == "__main__":
    create_simple_pdf()
