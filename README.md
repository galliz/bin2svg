# bin2svg

A Python library to convert binary (boolean) matrices to SVG.

## Installation

Clone the repository and install the package in editable mode:

```bash
pip install -e .
```

## Usage
```python
from bin2svg.converter import matrix_to_svg

matrix = [
    [1, 0, 1],
    [1, 0, 0],
    [1, 1, 1]
]
svg = matrix_to_svg(matrix)
print(svg)
```

Output:
```xml
<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 30 30">
<rect x="0" y="0" width="10" height="10" fill="#000" />
<rect x="20" y="0" width="10" height="10" fill="#000" />
<rect x="0" y="10" width="10" height="10" fill="#000" />
<rect x="0" y="20" width="10" height="10" fill="#000" />
<rect x="10" y="20" width="10" height="10" fill="#000" />
<rect x="20" y="20" width="10" height="10" fill="#000" />
</svg>
```

Visualized:

![Input matrix SVG](docs/example.svg)

### Optional arguments
- `cell_size (int, optional)`: Size of each cell in the SVG. Defaults to 10.
- `on_color (str, optional)`: Fill color for True cells. Defaults to "#000" (black).
- `off_color (Optional[str], optional)`: Fill color for the background (False cells). If provided, a full-background rectangle is drawn. Defaults to None.