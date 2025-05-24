# -*- coding: utf-8 -*-

"""Convert PDF to Markdown using marker-pdf.

You may pass a CSV file with the following format:
/path/to/pdf1.pdf, /path/to/markdown1.md
/path/to/pdf2.pdf, /path/to/markdown2.md

or you can pass the PDF and Markdown files as arguments.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from loguru import logger

from .align_tables import align_markdown_tables
from .converter import convert_pdf_to_markdown

logfile = Path("convert.log")
logger.add(logfile, level="ERROR", encoding="utf-8")


def _convert_single_file(
    pdf_path: Path, markdown_path: Path, force: bool = False
) -> None:
    """Convert a single PDF file to Markdown.

    Args:
        pdf_path: Path to the PDF file
        markdown_path: Path to the output Markdown file
        force: Whether to overwrite existing file
    """
    if markdown_path.exists() and not force:
        logger.info(
            f"Output file '{markdown_path}' already exists. Use -F to overwrite."
        )
        return

    try:
        md_text = convert_pdf_to_markdown(pdf_path)
        # Align tables for better readability
        md_text = align_markdown_tables(md_text)
        markdown_path.write_text(md_text, encoding="utf-8")
        logger.info(f"Converted '{pdf_path}' to '{markdown_path}'")
    except Exception as e:
        logger.error(f"Error converting '{pdf_path}': {e}")
        raise


def convert_batch(csv_file: Path, force: bool = False) -> None:
    """Convert multiple PDF files using a CSV file.

    Args:
        csv_file: Path to CSV file with PDF/Markdown pairs
        force: Whether to overwrite existing files
    """
    with csv_file.open("r") as f:
        for line in f:
            line = line.strip()
            if not line:  # Skip empty lines
                continue

            parts = line.split(",")
            if len(parts) != 2:
                logger.error(f"Invalid CSV line: {line}")
                continue

            pdf_path = Path(parts[0].strip())
            markdown_path = Path(parts[1].strip())

            try:
                _convert_single_file(pdf_path, markdown_path, force)
            except Exception:
                # Error already logged in _convert_single_file
                continue


def convert(
    pdf: Optional[Path] = None,
    markdown: Optional[Path] = None,
    *,
    file: Optional[Path] = None,
    force: bool = False,
) -> None:
    """Convert PDF to Markdown.

    Args:
        pdf: Path to single PDF file
        markdown: Path to output Markdown file
        file: Path to CSV file for batch conversion
        force: Whether to overwrite existing files
    """
    if file:
        convert_batch(file, force)
    elif pdf and markdown:
        _convert_single_file(pdf, markdown, force)
    else:
        logger.error("Please provide either PDF/Markdown paths or a CSV file.")
        sys.exit(1)


def main() -> None:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description="Convert PDF to Markdown")
    parser.add_argument("pdf", type=Path, nargs="?", help="Path to the PDF file")
    parser.add_argument(
        "markdown", type=Path, nargs="?", help="Path to the output Markdown file"
    )
    parser.add_argument("-f", "--file", type=Path, help="Path to CSV batch file")
    parser.add_argument(
        "-F",
        "--force",
        action="store_true",
        help="Force overwrite the output file(s) if it exists",
    )

    args = parser.parse_args()

    # Handle different argument combinations
    if args.file:
        if not args.file.exists():
            print(f"File '{args.file}' does not exist.")
            sys.exit(1)
        if not args.file.is_file():
            print(f"'{args.file}' is not a file.")
            sys.exit(1)
        if args.pdf or args.markdown:
            print("You can't specify both a CSV file and PDF/Markdown files.")
            sys.exit(1)

        convert(file=args.file, force=args.force)

    elif args.pdf and args.markdown:
        args.markdown.parent.mkdir(parents=True, exist_ok=True)
        convert(pdf=args.pdf, markdown=args.markdown, force=args.force)

    else:
        print("Please provide either PDF/Markdown files or a CSV file.")
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
