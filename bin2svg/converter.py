"""
Module for converting binary (boolean) matrices to SVG format.
"""

from typing import Optional
import numpy as np

__all__ = ["matrix_to_svg"]


def matrix_to_svg(
    matrix,
    cell_size: int = 10,
    on_color: str = "#000",
    off_color: Optional[str] = None,
    round: bool = False,
) -> str:
    """
    Convert a binary (boolean) matrix to an SVG string representation.

    Args:
        matrix (List[List[bool]]): 2D boolean matrix.
        cell_size (int, optional): Size of each cell. Defaults to 10.
        on_color (str, optional): Fill color for True cells. Defaults to "#000".
        off_color (Optional[str], optional): Background color if provided.
        round (bool, optional): Enables corner rounding. Defaults to False.

    Returns:
        str: SVG formatted string.
    """
    matrix = np.asarray(matrix)

    if matrix.size == 0 or matrix.shape[0] == 0 or matrix.shape[1] == 0:
        raise ValueError("Matrix must be non-empty and contain at least one cell.")
    height, width = matrix.shape

    # 1. Pad matrix with False cells around
    matrix_padded = np.pad(matrix, pad_width=1, mode="constant", constant_values=False)

    # 2. Create secondary matrix of sub-matrices, each cell being a 2x2 matrix representing the quadrants (corners) of each cell
    quadrants_matrix = np.zeros((height, width, 2, 2), dtype=bool)

    # 3. For each cell of original matrix
    for idx in np.ndindex(matrix.shape):
        i, j = idx

        # 3.1 If cell is True
        if matrix[idx] == True:
            # Set the cell's quadrants as True (default)
            quadrants_matrix[idx] = True

            # 3.1.1 Extract 3x3 neighborhood from matrix_padded
            neighborhood = matrix_padded[i : i + 3, j : j + 3]

            # 3.1.2 Set cell's quadrants based on neighborhood patterns
            if neighborhood[0, 1] == False and neighborhood[1, 0] == False:
                quadrants_matrix[idx][0, 0] = False

            if neighborhood[0, 1] == False and neighborhood[1, 2] == False:
                quadrants_matrix[idx][0, 1] = False

            if neighborhood[1, 2] == False and neighborhood[2, 1] == False:
                quadrants_matrix[idx][1, 1] = False

            if neighborhood[1, 0] == False and neighborhood[2, 1] == False:
                quadrants_matrix[idx][1, 0] = False

        # 3.2 If cell is False
        if matrix[idx] == False:
            # 3.2.1 Extract 3x3 neighborhood from matrix_padded
            neighborhood = matrix_padded[i : i + 3, j : j + 3]

            # 3.2.2 Set cell's quadrants based on neighborhood patterns
            if (
                neighborhood[0, 0] == True
                and neighborhood[0, 1] == True
                and neighborhood[1, 0] == True
            ):
                quadrants_matrix[idx][0, 0] = True

            if (
                neighborhood[0, 1] == True
                and neighborhood[0, 2] == True
                and neighborhood[1, 2] == True
            ):
                quadrants_matrix[idx][0, 1] = True

            if (
                neighborhood[1, 2] == True
                and neighborhood[2, 2] == True
                and neighborhood[2, 1] == True
            ):
                quadrants_matrix[idx][1, 1] = True

            if (
                neighborhood[1, 0] == True
                and neighborhood[2, 0] == True
                and neighborhood[2, 1] == True
            ):
                quadrants_matrix[idx][1, 0] = True

    # 4. Add SVG boilerplate
    svg_width = width * cell_size
    svg_height = height * cell_size
    svg_elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" '
        f'viewBox="0 0 {svg_width} {svg_height}">'
    ]

    if off_color is not None:
        svg_elements.append(f'<rect width="100%" height="100%" fill="{off_color}" />')

    # 5. For each cell, draw pre-made SVG patterns based on its quadrants matrix
    for idx in np.ndindex(matrix.shape):
        i, j = idx
        x = j * cell_size
        y = i * cell_size

        if matrix[idx] == True:

            # Draw squares for all True quadrants
            for qi, qj in [(0, 0), (0, 1), (1, 0), (1, 1)]:
                if quadrants_matrix[idx][qi, qj] == True:
                    qx = x + (qj * cell_size / 2)
                    qy = y + (qi * cell_size / 2)
                    svg_elements.append(
                        f'<rect x="{qx}" y="{qy}" width="{cell_size/2}" height="{cell_size/2}" fill="{on_color}" />'
                    )

            # Top left corner rounding
            if quadrants_matrix[idx][0, 0] == False:
                svg_elements.append(
                    f'<path d="M{x+cell_size/2},{y+cell_size/2} L{x},{y+cell_size/2} A{cell_size/2},{cell_size/2} 0 0 1 {x+cell_size/2},{y} Z" fill="{on_color}" />'
                )

            # Top right corner rounding
            if quadrants_matrix[idx][0, 1] == False:
                svg_elements.append(
                    f'<path d="M{x+cell_size/2},{y+cell_size/2} L{x+cell_size/2},{y} A{cell_size/2},{cell_size/2} 0 0 1 {x+cell_size},{y+cell_size/2} Z" fill="{on_color}" />'
                )

            # Bottom right corner rounding
            if quadrants_matrix[idx][1, 1] == False:
                svg_elements.append(
                    f'<path d="M{x+cell_size/2},{y+cell_size/2} L{x+cell_size},{y+cell_size/2} A{cell_size/2},{cell_size/2} 0 0 1 {x+cell_size/2},{y+cell_size} Z" fill="{on_color}" />'
                )

            # Bottom left corner rounding
            if quadrants_matrix[idx][1, 0] == False:
                svg_elements.append(
                    f'<path d="M{x+cell_size/2},{y+cell_size/2} L{x+cell_size/2},{y+cell_size} A{cell_size/2},{cell_size/2} 0 0 1 {x},{y+cell_size/2} Z" fill="{on_color}" />'
                )

        if matrix[idx] == False:
            # Inverted corner - Bottom right
            if quadrants_matrix[idx][1, 1] == True:
                svg_elements.append(
                    f'<path d="M{x+cell_size},{y+cell_size/2} V{y+cell_size} H{x+cell_size/2} A{cell_size/2},{cell_size/2} 0 0 0 {x+cell_size},{y+cell_size/2} Z" fill="{on_color}" />'
                )

            # Inverted corner - Bottom left
            if quadrants_matrix[idx][1, 0] == True:
                svg_elements.append(
                    f'<path d="M{x},{y+cell_size/2} V{y+cell_size} H{x+cell_size/2} A{cell_size/2},{cell_size/2} 0 0 1 {x},{y+cell_size/2} Z" fill="{on_color}" />'
                )

            # Inverted corner - Top right
            if quadrants_matrix[idx][0, 1] == True:
                svg_elements.append(
                    f'<path d="M{x+cell_size},{y+cell_size/2} V{y} H{x+cell_size/2} A{cell_size/2},{cell_size/2} 0 0 1 {x+cell_size},{y+cell_size/2} Z" fill="{on_color}" />'
                )

            # Inverted corner - Top left
            if quadrants_matrix[idx][0, 0] == True:
                svg_elements.append(
                    f'<path d="M{x},{y+cell_size/2} V{y} H{x+cell_size/2} A{cell_size/2},{cell_size/2} 0 0 0 {x},{y+cell_size/2} Z" fill="{on_color}" />'
                )

    svg_elements.append("</svg>")

    return "\n".join(svg_elements)


# For temporary testing purposes
if __name__ == "__main__":
    matrix = [
        [False, False, True, True],
        [True, True, False, True],
        [True, False, True, False],
        [True, True, True, True],
    ]
    print(matrix_to_svg(matrix))
