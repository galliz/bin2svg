import pytest
from bin2svg.converter import matrix_to_svg


def test_empty_matrix():
    # Empty matrix should raise ValueError.
    with pytest.raises(ValueError):
        matrix_to_svg([])
    # Matrix with an empty row should also raise ValueError.
    with pytest.raises(ValueError):
        matrix_to_svg([[]])


def test_inconsistent_rows():
    # Rows with different lengths should raise ValueError.
    matrix = [[True, False], [False]]
    with pytest.raises(ValueError):
        matrix_to_svg(matrix)


def test_svg_output_without_background():
    # For a valid matrix without background color, only True cells are drawn.
    matrix = [[True, False], [False, True]]
    cell_size = 10
    svg = matrix_to_svg(matrix, cell_size=cell_size, on_color="#ff0000")

    # Verify SVG tag dimensions.
    expected_width = 2 * cell_size
    expected_height = 2 * cell_size
    assert f'width="{expected_width}"' in svg
    assert f'height="{expected_height}"' in svg

    # Two rect elements for True cells should be present.
    assert svg.count("<rect") == 2
    # Ensure the on_color is applied.
    assert "#ff0000" in svg


def test_svg_output_with_background():
    # When an off_color is provided, a background rectangle is added.
    matrix = [[True, False], [False, True]]
    cell_size = 20
    svg = matrix_to_svg(
        matrix, cell_size=cell_size, on_color="black", off_color="white"
    )

    # Expect 1 background rect + 2 True-cell rects = 3 rect elements.
    assert svg.count("<rect") == 3
    # Verify the background rectangle uses the specified off_color.
    assert 'fill="white"' in svg
