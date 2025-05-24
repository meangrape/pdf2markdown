# rgs.get -*- coding: utf-8 -*-

"""Convert PDF to Markdown using pymupdf4llm. You may pass a CSV file with the following format:
/path/to/pdf1.pdf, /path/to/markdown1.md
/path/to/pdf2.pdf, /path/to/markdown2.md

or you can pass the PDF and Markdown files as arguments."""

import argparse
import sys
from pathlib import Path
from typing import Any, Optional

import pymupdf4llm
from loguru import logger

from .align_tables import align_markdown_tables

logfile = Path("convert.log")
logger.add(logfile, level="ERROR", encoding="utf-8")


def convert(*args: Optional[Any], **kwargs: Any) -> None:
    """Does the actual conversion.

    Args:
        args: The PDF and Markdown files to convert.
        kwargs: The keyword arguments. Can be a CSV file or force flag.
    """
    file: Any = kwargs.get("file")
    force: Any | bool = kwargs.get("force", False)
    markdown: Optional[Path | str] = None
    pdf: Optional[Path | str] = None

    if args and len(args) == 2:
        pdf = args[0]
        markdown = args[1]

    if file:
        with Path(file).open("r") as f:
            lines = f.readlines()
            for line in lines:
                pdf, markdown = line.strip().split(",")
                pdf = Path(pdf.strip())
                markdown = Path(markdown.strip())

                if markdown.exists() and not force:
                    logger.info(
                        f"Output file '{markdown}' already exists. Use -F to overwrite."
                    )
                    continue
                try:
                    md_text = pymupdf4llm.to_markdown(pdf)
                    # Align tables for better readability
                    md_text = align_markdown_tables(md_text)
                except Exception as e:
                    logger.error(f"Error converting '{pdf}': {e}")
                    continue
                markdown.write_bytes(md_text.encode("utf-8"))
                logger.info(f"Converted '{pdf}' to '{markdown}'")
        return

    else:
        if not args or len(args) < 2:
            logger.error("Please provide the PDF file and output Markdown file.")
            sys.exit(1)

        markdown = args[1]
        if markdown.exists() and not force:  # type: ignore
            logger.info(
                f"Output file '{markdown}' already exists. Use -F to overwrite."
            )
            sys.exit()

        md_text = pymupdf4llm.to_markdown(pdf)
        # Align tables for better readability
        md_text = align_markdown_tables(md_text)
        markdown.write_bytes(md_text.encode("utf-8"))  # type: ignore
        logger.info(f"Converted '{pdf}' to '{markdown}'")


def main() -> None:
    """We use print here instead of logger because in some cases we print the help message, and I prefer that the
    informational print statement don't have the loguru prefix."""

    parser = argparse.ArgumentParser(description="Convert PDF to Markdown")
    parser.add_argument("pdf", type=Path, help="Path to the PDF file")
    parser.add_argument("markdown", type=Path, help="Path to the output Markdown file")
    parser.add_argument("-f", "--file", type=Path, help="Path to CSV batch file")
    parser.add_argument(
        "-F",
        "--force",
        action="store_true",
        help="Force overwrite the output file(s) if it exists",
    )

    args = parser.parse_args()

    if len(sys.argv) == 0:
        print("Please provide the PDF file and output Markdown file or a CSV file.")
        parser.print_help()
        sys.exit()

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

    if args.pdf and args.markdown:
        args.markdown.parent.mkdir(parents=True, exist_ok=True)
        convert(args.pdf, args.markdown, force=args.force)

    else:
        print("Please provide both the PDF file and output Markdown file.")
        parser.print_help()
        sys.exit()


if __name__ == "__main__":
    main()
