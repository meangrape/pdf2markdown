[![Release](https://github.com/meangrape/pdf2markdown/actions/workflows/release.yml/badge.svg)](https://github.com/meangrape/pdf2markdown/actions/workflows/release.yml)

# pdf2markdown

A Python CLI tool that converts PDF files to Markdown format using pymupdf4llm.

## Features

- Convert single PDF files to Markdown
- Batch convert multiple PDFs using a CSV file
- Force overwrite existing output files
- Error logging for failed conversions
- Tries to preserves formatting including bold, italic, lists, and tables

# Limitations

- The tool may not perfectly preserve all formatting, especially for complex
  PDFs. I've had some problems with rows and headers.

## Installation

```bash
pip install pdf2markdown
```

## Usage

### Convert a single PDF

```bash
pdf2markdown input.pdf output.md
```

### Force overwrite existing output

```bash
pdf2markdown input.pdf output.md -F
```

### Batch convert using CSV file

Create a CSV file with PDF paths and output paths:

```csv
/path/to/pdf1.pdf, /path/to/markdown1.md
/path/to/pdf2.pdf, /path/to/markdown2.md
```

Then run:

```bash
pdf2markdown -f batch.csv
```

With force overwrite:

```bash
pdf2markdown -f batch.csv -F
```

## Options

- `-h, --help` - Show help message and exit
- `pdf` - Path to the PDF file to convert
- `markdown` - Path to the output Markdown file
- `-f, --file` - Path to CSV file for batch conversion
- `-F, --force` - Force overwrite existing output files

## Error Handling

Conversion errors are logged to `convert.log` in the current directory. The tool will continue processing remaining files in batch mode if one fails.

## Requirements

- Python >= 3.13
- pymupdf4llm >= 0.0.24
- loguru >= 0.7.3

## Development

Install development dependencies:

```bash
pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

## License

BSD 3-Clause License - see [LICENSE](LICENSE) file for details.

## Author

Jay Edwards <jay@meangrape.com>
