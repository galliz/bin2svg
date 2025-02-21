"""
Module for converting binary (boolean) matrices to SVG format.
"""

from typing import List, Optional

__all__ = ["matrix_to_svg"]


def matrix_to_svg(
    matrix: List[List[bool]],
    cell_size: int = 10,
    on_color: str = "#000",
    off_color: Optional[str] = None,
) -> str:
    """
    Convert a binary (boolean) matrix to an SVG string representation.

    Args:
        matrix (List[List[bool]]): 2D boolean matrix.
        cell_size (int, optional): Size of each cell in the SVG. Defaults to 10.
        on_color (str, optional): Fill color for True cells. Defaults to "#000" (black).
        off_color (Optional[str], optional): Fill color for the background (False cells).
                                             If provided, a full-background rectangle is drawn.
                                             Defaults to None.

    Returns:
        str: SVG formatted string.

    Raises:
        ValueError: If the matrix is empty or rows have inconsistent lengths.
    """
    if not matrix or not matrix[0]:
        raise ValueError("Matrix must be non-empty and contain at least one cell.")

    height = len(matrix)
    width = len(matrix[0])
    if any(len(row) != width for row in matrix):
        raise ValueError("All rows in the matrix must have the same length.")

    svg_width = width * cell_size
    svg_height = height * cell_size
    svg_elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" '
        f'viewBox="0 0 {svg_width} {svg_height}">'
    ]

    if off_color is not None:
        svg_elements.append(f'<rect width="100%" height="100%" fill="{off_color}" />')

    for i, row in enumerate(matrix):
        for j, cell in enumerate(row):
            if cell:
                x = j * cell_size
                y = i * cell_size
                svg_elements.append(
                    f'<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" fill="{on_color}" />'
                )

    svg_elements.append("</svg>")
    return "\n".join(svg_elements)
