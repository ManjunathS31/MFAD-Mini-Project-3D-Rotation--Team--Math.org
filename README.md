# 3D Rotation Using Orthogonal Matrices

MFAD Mini Project | Team- Math.org

**Team members:** 
MANJUNATH.S - PES1UG25AM203
NAGESH B R - PES1UG25AM229
Mohammed Taqui Shujath - PES1UG25AM218
MONINGI VAISHNAV RAJ - PES1UG25AM222                        
 
## About the project
This project shows how orthogonal matrices rotate 3D objects without changing their shape or size. Rotations about the X, Y and Z axes are combined into one matrix R = Rx · Ry · Rz, which is applied to the vertices of 3D shapes.

The project checks the key properties of a rotation matrix:
- Orthogonality: Rᵀ R = I
- Determinant = +1 (a proper rotation)
- Distances and edge lengths are preserved

## Files
| File | Description |
|------|-------------|
| `rotation_project_shapes.py` | Python program. Choose a shape and angles, and it prints the matrices, original and rotated coordinates and the verification checks, saves a CSV, and plots the shapes in 3D. |
| `rotation_lab.html` | Interactive web demo (Rotation Lab). Move the sliders to rotate 10 objects and see the matrix and checks update live. |

## How to run

**Python script**
pip install numpy pandas matplotlib
python rotation_project_shapes.py

**Web demo**
Download `rotation_lab.html` and open it in any browser. No installation is needed.

## Tools used
Python (NumPy, Pandas, Matplotlib), HTML, CSS, JavaScript
