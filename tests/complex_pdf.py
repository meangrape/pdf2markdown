# -*- coding: utf-8 -*-
"""Create a complex PDF document with images, tables, and custom styles using ReportLab."""

import os
import sys
from pathlib import Path
from typing import Optional

from PIL import Image as PILImage
from PIL import ImageDraw
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (Image, PageBreak, Paragraph, SimpleDocTemplate,
                                Spacer, Table, TableStyle)
from reportlab.platypus.flowables import Flowable


def create_image(filename="dummy_image.png", width=200, height=150) -> Optional[Path]:
    """Creates an image to be inserted into the PDF.

    Args:
        filename (str): The name of the image file to create.
        width (int): The width of the image.
        height (int): The height of the image.
    """

    image = PILImage.new('RGB', (width, height), color = (73, 109, 137))
    d = ImageDraw.Draw(image)
    d.text((10,10), "Dummy Image", fill=(255,255,0))
    try:
        image.save(filename)
    except Exception as e:
        print(f"Error creating image: {e}", file=sys.stderr)
        return None
    print(f"Created dummy image: {filename}")
    return Path(filename)


class HeaderAndFooter(Flowable):
    """
    Custom Flowable for header/footer (more common with PageTemplate, but showing here). When testing with
    is_header=True, the converter didn't pick up the element. It works fine with is_header=False.
    """
    def __init__(self, text, is_header=True):
        Flowable.__init__(self)
        self.text = text
        self.is_header = is_header

    def draw(self):
        self.canv.saveState()
        self.canv.setFont("Helvetica", 9)
        if self.is_header:
            self.canv.drawString(inch, letter[1] - 0.5 * inch, self.text) # Top right
        else:
            self.canv.drawString(inch, 0.75 * inch, self.text) # Bottom right
        self.canv.restoreState()


def create_complex_pdf(filename="complex_document.pdf", image_filename="complex_image.png"): # MODIFIED
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Custom styles
    heading_style = ParagraphStyle(
        "HeadingStyle",
        parent=styles["h2"],
        fontSize=18,
        spaceAfter=0.2 * inch,
        alignment=TA_CENTER
    )
    body_style = ParagraphStyle(
        "BodyStyle",
        parent=styles["Normal"],
        fontSize=10,
        leading=14, # Line spacing
        spaceAfter=0.1 * inch,
        alignment=TA_LEFT
    )

    # --- Section 1: Title and Introduction ---
    story.append(Paragraph("<u><b>Complex PDF Document Example</b></u>", styles['h1']))
    story.append(Spacer(1, 0.4 * inch))
    story.append(Paragraph("This document demonstrates more advanced features of PDF generation using ReportLab.", body_style))
    story.append(Spacer(1, 0.2 * inch))

    # --- Section 2: Image Inclusion ---
    story.append(Paragraph("Image Example:", heading_style))

    image_path = image_filename
    if not os.path.exists(image_path):
        image_path = create_image(filename=image_path)

    if image_path:
        image = Image(image_path, width=3*inch, height=2.5*inch)
        story.append(image)
        story.append(Paragraph("<i>A placeholder image demonstrating embedding.</i>", styles["Italic"]))
        story.append(Spacer(1, 0.3 * inch))
    else:
        story.append(Paragraph("<i>Image could not be loaded.</i>", styles["Italic"]))

    # --- Section 3: Data Table ---
    story.append(Paragraph("Table Example:", heading_style))
    data = [
        ["Header 1", "Header 2", "Header 3", "Header 4"],
        ["Row 1 Col 1", "Row 1 Col 2", "Row 1 Col 3", "Row 1 Col 4"],
        ["Row 2 Col 1", "Row 2 Col 2", "Row 2 Col 3", "Row 2 Col 4"],
        ["Row 3 Col 1", "Row 3 Col 2", "Row 3 Col 3", "Row 3 Col 4 with more text"],
    ]
    table = Table(data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey), # Header row background
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke), # Header text color
        ("ALIGN", (0, 0), (-1, -1), "CENTER"), # All cells centered
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), # Header font
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12), # Header padding
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige), # Body background
        ("GRID", (0, 0), (-1, -1), 1, colors.black), # All borders
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"), # Vertical align
    ]))
    story.append(table)
    story.append(Spacer(1, 0.3 * inch))

    # --- Section 4: Page Break and New Page Content ---
    story.append(PageBreak()) # Forces a new page
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph("This is content on the <b>second page</b>, demonstrating page breaks.", body_style))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("We can continue with more elaborate layouts here, potentially mixing elements like images and tables freely across pages.", body_style))

    # Add a footer (this is a simplified way; PageTemplate is better for full dynamic headers/footers)
    story.append(HeaderAndFooter("Generated by ReportLab", is_header=False))

    # Build the PDF
    doc.build(story)


if __name__ == "__main__":
    create_complex_pdf()
