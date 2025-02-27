"""
Module for converting binary (boolean) matrices to SVG format.
"""

from typing import List, Optional
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

    return matrix_padded


# For temporary testing purposes
if __name__ == "__main__":
    matrix = [[True, False], [False, True]]
    print(matrix_to_svg(matrix))
