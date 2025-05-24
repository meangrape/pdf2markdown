# -*- coding: utf-8 -*-

"""PDF to Markdown conversion using marker-pdf."""

import subprocess
import tempfile
from pathlib import Path

from loguru import logger


def convert_pdf_to_markdown(pdf_path: Path) -> str:
    """Convert PDF to markdown using marker.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        Markdown text

    Raises:
        RuntimeError: If marker-pdf is not installed or conversion fails
        FileNotFoundError: If the output file is not found
    """
    logger.info("Converting PDF with marker...")

    try:
        # Create temporary output directory
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Run marker_single command
            cmd = [
                "marker_single",
                str(pdf_path),
                "--output_dir",
                str(temp_path),
                "--output_format",
                "markdown",
                "--disable_multiprocessing",  # More stable for single file
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=None)

            if result.returncode != 0:
                logger.error(f"Marker command failed: {result.stderr}")
                raise RuntimeError(f"Marker conversion failed: {result.stderr}")

            # Find the generated markdown file
            output_name = pdf_path.stem

            # Try with subdirectory first (common pattern)
            md_file = temp_path / output_name / f"{output_name}.md"
            if md_file.exists():
                return md_file.read_text()

            # Try without subdirectory
            md_file = temp_path / f"{output_name}.md"
            if md_file.exists():
                return md_file.read_text()

            # File not found at either location
            logger.error("Could not find output file at expected locations")
            raise FileNotFoundError("Marker output file not found")

    except FileNotFoundError as e:
        if "marker_single" in str(e):
            logger.error("marker_single command not found. Is marker-pdf installed?")
            raise RuntimeError(
                "marker-pdf is not installed. Install with: pip install marker-pdf"
            ) from e
        raise
    except Exception as e:
        logger.error(f"Error with marker conversion: {e}")
        raise
