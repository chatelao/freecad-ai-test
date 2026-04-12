import sys
import os

# Import utility
from freecad_utils import setup_freecad

if not setup_freecad():
    print("FreeCAD not found. Exiting.")
    sys.exit(1)

import FreeCAD
import Part
import Mesh

def verify():
    if not os.path.exists("benchy.stl"):
        print("benchy.stl not found.")
        return False

    mesh = Mesh.read("benchy.stl")
    bound_box = mesh.BoundBox

    print(f"Bounding Box: {bound_box}")
    print(f"Length (X): {bound_box.XLength:.2f} mm")
    print(f"Width (Y): {bound_box.YLength:.2f} mm")
    print(f"Height (Z): {bound_box.ZLength:.2f} mm")

    # Standard dimensions
    target_l = 60.0
    target_w = 31.0
    target_h = 48.0

    # Check 99.5% accuracy (threshold 0.5%)
    tol = 0.005

    def check_dim(actual, target, name):
        diff = abs(actual - target) / target
        if diff > tol:
            print(f"FAIL: {name} deviation {diff*100:.2f}% exceeds {tol*100:.2f}%")
            return False
        else:
            print(f"PASS: {name} deviation {diff*100:.2f}%")
            return True

    success = True
    success &= check_dim(bound_box.XLength, target_l, "Length")
    success &= check_dim(bound_box.YLength, target_w, "Width")
    success &= check_dim(bound_box.ZLength, target_h, "Height")

    if success:
        print("Overall Accuracy within 99.5%")
    else:
        print("Accuracy check failed.")

    return success

if __name__ == "__main__":
    verify()
