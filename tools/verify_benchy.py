import sys
import os

# Setup FreeCAD path
from freecad_utils import setup_freecad
if not setup_freecad():
    print("FreeCAD library not found!")
    sys.exit(1)

import FreeCAD
import Mesh

def verify_benchy(stl_path):
    if not os.path.exists(stl_path):
        print(f"File not found: {stl_path}")
        return False

    mesh = Mesh.read(stl_path)
    bbox = mesh.BoundBox

    length = bbox.XMax - bbox.XMin
    width = bbox.YMax - bbox.YMin
    height = bbox.ZMax - bbox.ZMin

    print(f"Model Dimensions:")
    print(f"  Length: {length:.2f} mm (Expected: 60.00)")
    print(f"  Width:  {width:.2f} mm (Expected: 31.00)")
    print(f"  Height: {height:.2f} mm (Expected: 48.00)")

    # Check 99.5% accuracy
    l_acc = 1.0 - abs(length - 60.0) / 60.0
    w_acc = 1.0 - abs(width - 31.0) / 31.0
    h_acc = 1.0 - abs(height - 48.0) / 48.0

    print(f"Accuracy:")
    print(f"  Length: {l_acc*100:.2f}%")
    print(f"  Width:  {w_acc*100:.2f}%")
    print(f"  Height: {h_acc*100:.2f}%")

    if l_acc >= 0.995 and w_acc >= 0.995 and h_acc >= 0.995:
        print("Model meets 99.5% accuracy requirement for overall dimensions.")
        return True
    else:
        print("Model DOES NOT meet 99.5% accuracy requirement.")
        return False

if __name__ == "__main__":
    stl_file = "benchy.stl"
    if len(sys.argv) > 1:
        stl_file = sys.argv[1]

    verify_benchy(stl_file)
