# -*- coding: utf-8 -*-

"""Functions for aligning tables in markdown content."""

import re
from typing import List


def align_markdown_tables(content: str) -> str:
    """Aligns tables in markdown content for better readability.

    Args:
        content: The markdown content containing tables

    Returns:
        The markdown content with aligned tables
    """
    lines = content.split("\n")
    result: List[str] = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Check if this is the start of a table
        if "|" in line and i + 1 < len(lines) and "|" in lines[i + 1] and re.match(r"^[\s\-:|]+$", lines[i + 1]):
            # Found a table
            table_lines: List[str] = []
            j = i

            while j < len(lines) and "|" in lines[j]:
                table_lines.append(lines[j])
                j += 1

            if len(table_lines) >= 2:  # At least header and separator
                table_data: List[List[str]] = []
                for table_line in table_lines:
                    cells = [cell.strip() for cell in table_line.split("|")]
                    # Remove empty cells at start and end
                    if cells and cells[0] == "":
                        cells = cells[1:]
                    if cells and cells[-1] == "":
                        cells = cells[:-1]
                    table_data.append(cells)

                # Find maximum width for each column
                num_cols = max(len(row) for row in table_data)
                col_widths = [0] * num_cols

                for row in table_data:
                    for idx, cell in enumerate(row):
                        if idx < num_cols:
                            # For separator row, count dashes
                            if re.match(r"^[\-:]+$", cell):
                                col_widths[idx] = max(col_widths[idx], 3)  # Minimum 3 for separator
                            else:
                                col_widths[idx] = max(col_widths[idx], len(cell))

                # Generate aligned table
                aligned_table: List[str] = []
                for row_idx, row in enumerate(table_data):
                    aligned_cells = []
                    for col_idx in range(num_cols):
                        if col_idx < len(row):
                            cell = row[col_idx]
                            if row_idx == 1 and re.match(r"^[\-:]+$", cell):  # Separator row
                                # Preserve alignment indicators
                                match (cell.startswith(":"), cell.endswith(":")):
                                    case (True, True):  # Center aligned
                                        aligned_cells.append(":" + "-" * (col_widths[col_idx] - 2) + ":")
                                    case (True, False):  # Left aligned
                                        aligned_cells.append(":" + "-" * (col_widths[col_idx] - 1))
                                    case (False, True):  # Right aligned
                                        aligned_cells.append("-" * (col_widths[col_idx] - 1) + ":")
                                    case (False, False):  # No alignment
                                        aligned_cells.append("-" * col_widths[col_idx])
                            else:
                                aligned_cells.append(cell.ljust(col_widths[col_idx]))
                        else:
                            aligned_cells.append(" " * col_widths[col_idx])

                    aligned_table.append("| " + " | ".join(aligned_cells) + " |")

                result.extend(aligned_table)
                i = j
                continue

        result.append(line)
        i += 1

    return "\n".join(result)
