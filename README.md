# Ray Tracing and Projection

This project includes Python scripts for basic computer graphics techniques including ray tracing, 3D-to-2D projection, and 2D shape visualization.

## Requirements

Install all necessary dependencies with:

```bash
pip install numpy matplotlib pillow
```

## File Overview

### RayTracing.py
Performs ray tracing to render a 3D scene with spheres, a white plane, and a face mesh.

- Input: `face-vertices.data` or `face-vertices copy.data`
- Output: Rendered image (e.g., `output.png`)
- Run:
  ```bash
  python RayTracing.py
  ```

### Projection.py
Projects 3D vertices onto a 2D plane using orthographic or perspective projection.

- Input: `face-vertices.data`
- Output: 2D plot displayed with Matplotlib
- Run:
  ```bash
  python Projection.py
  ```

### face-vertices.data / face-vertices copy.data
These files contain 3D vertex coordinates of a face mesh.

- Used by: `RayTracing.py` and `Projection.py`
- Format: Likely one vertex per line (e.g., `x y z`)
- Do not run directly.

### Circle.py
Generates and displays a 2D circle using NumPy and Matplotlib.

- Output: A Matplotlib window displaying a circle.
- Run:
  ```bash
  python Circle.py
  ```

## Notes

- These scripts are designed to be run from the command line or a Python IDE such as Visual Studio Code.
- Ensure that the `.data` files are located in the same directory as the scripts.
- This code is intended for educational and experimental use.
