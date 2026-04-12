import os
import sys

# Setup FreeCAD path
from freecad_utils import setup_freecad
if not setup_freecad():
    sys.exit(1)

import FreeCAD
import Mesh

def validate_stl(filepath):
    """Validates the STL file for bounding box and integrity."""
    if not os.path.exists(filepath):
        print(f"Error: {filepath} does not exist.")
        return False

    try:
        # Using Mesh.read as per memory recommendation for headless envs
        mesh = Mesh.read(filepath)
        bbox = mesh.BoundBox

        length = bbox.XMax - bbox.XMin
        width = bbox.YMax - bbox.YMin
        height = bbox.ZMax - bbox.ZMin

        print(f"STL Bounding Box: Length={length:.2f}, Width={width:.2f}, Height={height:.2f}")

        # Standard dimensions: 60x31x48
        # Check if within 99.5% (0.5% tolerance)
        tol = 0.005

        target_l, target_w, target_h = 60.0, 31.0, 48.0

        l_ok = abs(length - target_l) / target_l <= tol
        w_ok = abs(width - target_w) / target_w <= tol
        h_ok = abs(height - target_h) / target_h <= tol

        if l_ok and w_ok and h_ok:
            print("Validation PASSED: Dimensions are within 0.5% tolerance.")
            return True
        else:
            print("Validation FAILED: Dimensions are outside tolerance.")
            if not l_ok: print(f"  Length deviation: {abs(length - target_l):.2f} mm")
            if not w_ok: print(f"  Width deviation: {abs(width - target_w):.2f} mm")
            if not h_ok: print(f"  Height deviation: {abs(height - target_h):.2f} mm")
            return False

    except Exception as e:
        print(f"Error during STL validation: {e}")
        return False

def main():
    stl_path = "output/benchy.stl"
    if validate_stl(stl_path):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
