import os
import sys

from freecad_utils import setup_freecad

FreeCAD, Part, PartDesign, Mesh, TechDraw = setup_freecad()

def verify_benchy(stl_path):
    print(f"Verifying {stl_path}...")

    # Load the mesh
    mesh = Mesh.Mesh(stl_path)

    # Get bounding box
    bbox = mesh.BoundBox

    length = bbox.XLength
    width = bbox.YLength
    height = bbox.ZLength

    print(f"Dimensions: {length:.2f} x {width:.2f} x {height:.2f} mm")

    # Standard dimensions: 60 x 31 x 48 mm
    tolerance = 2.0

    target_l, target_w, target_h = 60.0, 31.0, 48.0

    success = True
    if abs(length - target_l) > tolerance:
        print(f"Warning: Length {length:.2f} deviates from {target_l}")
        success = False
    if abs(width - target_w) > tolerance:
        print(f"Warning: Width {width:.2f} deviates from {target_w}")
        success = False
    if abs(height - target_h) > tolerance:
        print(f"Warning: Height {height:.2f} deviates from {target_h}")
        success = False

    if success:
        print("Model dimensions are within tolerance.")
    else:
        print("Model dimensions are OUTSIDE of tolerance.")

    return success

if __name__ == "__main__":
    # Check common locations for benchy.stl
    possible_paths = [
        "output/benchy.stl",
        "benchy.stl"
    ]

    stl_file = None
    for path in possible_paths:
        if os.path.exists(path):
            stl_file = path
            break

    if stl_file:
        verify_benchy(stl_file)
    else:
        print("Error: benchy.stl not found in any of the expected locations.")
        sys.exit(1)
