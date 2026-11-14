import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.set_printoptions(precision=3, suppress=True)

# Each shape is represented by its vertices (3D points) and the edges joining them.
SHAPES = {
    "1": ("Cube", np.array([
        [-1,-1,-1], [1,-1,-1], [1,1,-1], [-1,1,-1],
        [-1,-1,1], [1,-1,1], [1,1,1], [-1,1,1]
    ], dtype=float), [
        (0,1),(1,2),(2,3),(3,0),(4,5),(5,6),
        (6,7),(7,4),(0,4),(1,5),(2,6),(3,7)
    ]),
    "2": ("Cuboid", np.array([
        [-1.5,-1,-0.6], [1.5,-1,-0.6], [1.5,1,-0.6], [-1.5,1,-0.6],
        [-1.5,-1,0.6], [1.5,-1,0.6], [1.5,1,0.6], [-1.5,1,0.6]
    ], dtype=float), [
        (0,1),(1,2),(2,3),(3,0),(4,5),(5,6),
        (6,7),(7,4),(0,4),(1,5),(2,6),(3,7)
    ]),
    "3": ("Tetrahedron", np.array([
        [1,1,1], [-1,-1,1], [-1,1,-1], [1,-1,-1]
    ], dtype=float), [
        (0,1),(0,2),(0,3),(1,2),(1,3),(2,3)
    ]),
    "4": ("Octahedron / Diamond", np.array([
        [1,0,0], [-1,0,0], [0,1,0], [0,-1,0], [0,0,1], [0,0,-1]
    ], dtype=float), [
        (0,2),(0,3),(0,4),(0,5),(1,2),(1,3),(1,4),(1,5),
        (2,4),(2,5),(3,4),(3,5)
    ]),
    "5": ("Square Pyramid", np.array([
        [-1,-1,-1], [1,-1,-1], [1,1,-1], [-1,1,-1], [0,0,1.4]
    ], dtype=float), [
        (0,1),(1,2),(2,3),(3,0),(0,4),(1,4),(2,4),(3,4)
    ]),
    "6": ("Triangular Prism", np.array([
        [-1,-0.8,-1], [1,-0.8,-1], [0,1,-1],
        [-1,-0.8,1], [1,-0.8,1], [0,1,1]
    ], dtype=float), [
        (0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(0,3),(1,4),(2,5)
    ]),
}


def rotation_matrices(angle_x, angle_y, angle_z):
    x, y, z = np.radians([angle_x, angle_y, angle_z])
    rx = np.array([[1, 0, 0], [0, np.cos(x), -np.sin(x)], [0, np.sin(x), np.cos(x)]])
    ry = np.array([[np.cos(y), 0, np.sin(y)], [0, 1, 0], [-np.sin(y), 0, np.cos(y)]])
    rz = np.array([[np.cos(z), -np.sin(z), 0], [np.sin(z), np.cos(z), 0], [0, 0, 1]])
    return rx, ry, rz, rx @ ry @ rz


def draw_3d(axis, points, edges, title, limits):
    for start, end in edges:
        axis.plot(points[[start, end], 0], points[[start, end], 1], points[[start, end], 2], linewidth=2)
    axis.scatter(points[:, 0], points[:, 1], points[:, 2], s=28)
    axis.set_title(title, fontweight="bold")
    axis.set_xlabel("X")
    axis.set_ylabel("Y")
    axis.set_zlabel("Z")
    axis.set_xlim(-limits, limits)
    axis.set_ylim(-limits, limits)
    axis.set_zlim(-limits, limits)
    axis.set_box_aspect((1, 1, 1))
    axis.grid(True)


def draw_projection(axis, points, edges, title):
    projected = points[:, :2]  # 2D projection formed by dropping Z
    for start, end in edges:
        axis.plot(projected[[start, end], 0], projected[[start, end], 1], linewidth=2)
    axis.scatter(projected[:, 0], projected[:, 1], s=28)
    axis.set_title(title, fontweight="bold")
    axis.set_xlabel("Projected X")
    axis.set_ylabel("Projected Y")
    axis.set_aspect("equal", adjustable="box")
    axis.grid(True)


def main():
    print("=" * 62)
    print("       3D ROTATION USING ORTHOGONAL MATRICES")
    print("=" * 62)
    print("Choose a shape:")
    for key, (name, _, _) in SHAPES.items():
        print(f"  {key}. {name}")

    choice = input("Enter shape number (1-6): ").strip()
    if choice not in SHAPES:
        print("Invalid choice. Please run again and choose a number from 1 to 6.")
        return

    shape_name, vertices, edges = SHAPES[choice]
    try:
        ax = float(input("Enter rotation angle around X axis (degrees): "))
        ay = float(input("Enter rotation angle around Y axis (degrees): "))
        az = float(input("Enter rotation angle around Z axis (degrees): "))
    except ValueError:
        print("Please enter valid numbers, such as 30, 45 and 20.")
        return

    rx, ry, rz, rotation = rotation_matrices(ax, ay, az)
    rotated = vertices @ rotation.T  # Vertices are row vectors.

    print(f"\nSelected shape: {shape_name}")
    print("\nRotation matrix Rx:\n", rx)
    print("\nRotation matrix Ry:\n", ry)
    print("\nRotation matrix Rz:\n", rz)
    print("\nCombined matrix R = Rx @ Ry @ Rz:\n", rotation)

    original_df = pd.DataFrame(vertices, columns=["X", "Y", "Z"])
    rotated_df = pd.DataFrame(rotated, columns=["Rotated X", "Rotated Y", "Rotated Z"])
    results = pd.concat([original_df.add_prefix("Original "), rotated_df], axis=1).round(3)
    print("\nOriginal and rotated vertex coordinates:")
    print(results.to_string(index=False))

    identity_check = rotation.T @ rotation
    determinant = np.linalg.det(rotation)
    orthogonality_error = np.max(np.abs(identity_check - np.eye(3)))
    before_lengths = np.linalg.norm(vertices, axis=1)
    after_lengths = np.linalg.norm(rotated, axis=1)
    length_error = np.max(np.abs(before_lengths - after_lengths))
    print("\nOrthogonality check R.T @ R:\n", np.round(identity_check, 3))
    print(f"Maximum identity-check error: {orthogonality_error:.8f}")
    print(f"Determinant of R: {determinant:.6f} (should be +1)")
    print(f"Maximum change in distance from origin: {length_error:.8f}")

    filename = f"{shape_name.lower().replace(' ', '_').replace('/', '_')}_rotation_results.csv"
    results.to_csv(filename, index=False)
    print(f"\nSaved coordinate table as {filename}")

    max_coord = max(2.0, float(np.max(np.abs(np.vstack([vertices, rotated])))) * 1.25)
    fig = plt.figure(figsize=(13, 9))
    fig.suptitle(f"3D Rotation of {shape_name} | X={ax:g}°, Y={ay:g}°, Z={az:g}°", fontsize=15, fontweight="bold")
    a1 = fig.add_subplot(221, projection="3d")
    a2 = fig.add_subplot(222, projection="3d")
    a3 = fig.add_subplot(223)
    a4 = fig.add_subplot(224)
    draw_3d(a1, vertices, edges, f"Original {shape_name}", max_coord)
    draw_3d(a2, rotated, edges, f"Rotated {shape_name}", max_coord)
    draw_projection(a3, vertices, edges, "Original 2D Projection (drop Z)")
    draw_projection(a4, rotated, edges, "Rotated 2D Projection (drop Z)")
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()


if __name__ == "__main__":
    main()
