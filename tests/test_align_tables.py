# -*- coding: utf-8 -*-
"""Tests for the align_tables module."""

from pathlib import Path

from pdf2markdown.align_tables import align_markdown_tables


def test_align_tables(tmp_path: Path) -> None:
    """Test that align_markdown_tables properly aligns markdown tables."""

    # Create a markdown file with a misaligned table
    misaligned_content = """# Test Document

Here is some text before the table.

|Header 1|Header 2|Header 3|
|---|---|---|
|Short|This is a longer cell|Med|
|Row 2 Column 1|B|C|
|A|B|This is the longest cell in the table|

Some text after the table.

Another table:

|Name|Age|City|
|---|---:|:---:|
|John Doe|25|New York|
|Jane|30|Los Angeles|
|Bob Smith|45|Chicago|

End of document.
"""

    # Expected aligned output
    expected_content = """# Test Document

Here is some text before the table.

| Header 1       | Header 2              | Header 3                              |
| -------------- | --------------------- | ------------------------------------- |
| Short          | This is a longer cell | Med                                   |
| Row 2 Column 1 | B                     | C                                     |
| A              | B                     | This is the longest cell in the table |

Some text after the table.

Another table:

| Name      | Age | City        |
| --------- | --: | :---------: |
| John Doe  | 25  | New York    |
| Jane      | 30  | Los Angeles |
| Bob Smith | 45  | Chicago     |

End of document.
"""

    # Run the alignment function
    aligned_content = align_markdown_tables(misaligned_content)

    # Compare the output
    assert aligned_content == expected_content

    # Also test with a file
    test_file = tmp_path / "test_align.md"
    test_file.write_text(misaligned_content)

    # Read, align, and write back
    content = test_file.read_text()
    aligned = align_markdown_tables(content)
    test_file.write_text(aligned)

    # Verify file content
    assert test_file.read_text() == expected_content


def test_align_tables_no_tables() -> None:
    """Test that content without tables is unchanged."""
    content = """# Document without tables

This is a paragraph.

## Another section

More text here.
"""

    aligned = align_markdown_tables(content)
    assert aligned == content


def test_align_tables_edge_cases() -> None:
    """Test edge cases for table alignment."""

    # Table with empty cells
    content_empty_cells = """|A||C|
|---|---|---|
|1||3|
||2||
"""

    expected_empty_cells = """| A   |     | C   |
| --- | --- | --- |
| 1   |     | 3   |
|     | 2   |     |
"""

    assert align_markdown_tables(content_empty_cells).strip() == expected_empty_cells.strip()

    # Single column table
    single_col = """|Header|
|---|
|Value 1|
|Value 2|
"""

    expected_single = """| Header  |
| ------- |
| Value 1 |
| Value 2 |
"""

    assert align_markdown_tables(single_col).strip() == expected_single.strip()
