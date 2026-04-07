import sys
import os

# Import setup_freecad from freecad_utils
sys.path.append(os.path.join(os.path.dirname(__file__)))
from freecad_utils import setup_freecad

if not setup_freecad():
    print("Failed to initialize FreeCAD. Exiting.")
    sys.exit(1)

import Mesh

def verify_benchy(stl_path):
    if not os.path.exists(stl_path):
        # Check root as well
        stl_path = os.path.basename(stl_path)
        if not os.path.exists(stl_path):
            print(f"Error: {stl_path} not found.")
            return False

    mesh = Mesh.Mesh(stl_path)
    bbox = mesh.BoundBox

    print(f"Bounding Box for {stl_path}:")
    print(f"  X: {bbox.XMin:.2f} to {bbox.XMax:.2f} (Length: {bbox.XLength:.2f} mm)")
    print(f"  Y: {bbox.YMin:.2f} to {bbox.YMax:.2f} (Width: {bbox.YLength:.2f} mm)")
    print(f"  Z: {bbox.ZMin:.2f} to {bbox.ZMax:.2f} (Height: {bbox.ZLength:.2f} mm)")

    # Validation against specifications
    # Length: 60mm, Width: 31mm, Height: 48mm

    errors = []
    if not (59.0 <= bbox.XLength <= 61.0):
        errors.append(f"Length mismatch: {bbox.XLength:.2f} mm (expected ~60.00 mm)")
    if not (30.0 <= bbox.YLength <= 32.0):
        errors.append(f"Width mismatch: {bbox.YLength:.2f} mm (expected ~31.00 mm)")
    if not (47.0 <= bbox.ZLength <= 49.0):
        errors.append(f"Height mismatch: {bbox.ZLength:.2f} mm (expected ~48.50 mm)")

    if errors:
        print("Validation FAILED:")
        for e in errors:
            print(f"  - {e}")
        return False
    else:
        print("Validation PASSED.")
        return True

if __name__ == "__main__":
    stl_to_check = "benchy.stl"
    if not verify_benchy(stl_to_check):
        sys.exit(1)
