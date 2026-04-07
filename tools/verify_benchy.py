import os
import sys

# Add tools directory to path to import freecad_utils
sys.path.append(os.path.dirname(__file__))
import freecad_utils

if not freecad_utils.setup_freecad_path():
    print("Error: Could not find FreeCAD library.")
    sys.exit(1)

import FreeCAD
import Mesh

def verify_benchy(stl_path):
    if not os.path.exists(stl_path):
        print(f"Error: STL file not found at {stl_path}")
        return False

    mesh = Mesh.read(stl_path)
    bbox = mesh.BoundBox

    # Standard 3DBenchy dimensions
    expected_length = 60.0
    expected_width = 31.0
    expected_height = 48.0 # Total height with chimney as per specs

    print(f"Verifying {stl_path} dimensions:")
    print(f"  Length: {bbox.XLength:.2f} mm (Expected ~{expected_length})")
    print(f"  Width:  {bbox.YLength:.2f} mm (Expected ~{expected_width})")
    print(f"  Height: {bbox.ZLength:.2f} mm (Expected ~{expected_height})")

    # Tolerances
    tol = 1.0

    length_ok = abs(bbox.XLength - expected_length) < tol
    width_ok = abs(bbox.YLength - expected_width) < tol
    height_ok = abs(bbox.ZLength - expected_height) < tol

    if length_ok and width_ok and height_ok:
        print("Verification SUCCESS: Model dimensions are within tolerance.")
        return True
    else:
        print("Verification FAILURE: Model dimensions are outside tolerance.")
        if not length_ok: print(f"  Length mismatch: {bbox.XLength:.2f} != {expected_length}")
        if not width_ok: print(f"  Width mismatch: {bbox.YLength:.2f} != {expected_width}")
        if not height_ok: print(f"  Height mismatch: {bbox.ZLength:.2f} != {expected_height}")
        return False

if __name__ == "__main__":
    stl_path = "benchy.stl"
    if not os.path.exists(stl_path):
        stl_path = os.path.join("output", "benchy.stl")

    if verify_benchy(stl_path):
        sys.exit(0)
    else:
        sys.exit(1)
