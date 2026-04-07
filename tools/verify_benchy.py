import sys
import os

# Add the path to FreeCAD
from freecad_utils import setup_freecad
if not setup_freecad():
    print("FreeCAD not found")
    sys.exit(1)

import FreeCAD
import Mesh

def verify_benchy():
    stl_path = "output/benchy.stl"
    if not os.path.exists(stl_path):
        # Check root too
        stl_path = "benchy.stl"
        if not os.path.exists(stl_path):
            print("STL file not found")
            return False

    mesh = Mesh.read(stl_path)
    bound_box = mesh.BoundBox

    length = bound_box.XLength
    width = bound_box.YLength
    height = bound_box.ZLength

    print(f"Measured Dimensions:")
    print(f"Length: {length:.2f} mm")
    print(f"Width: {width:.2f} mm")
    print(f"Height: {height:.2f} mm")

    target_length = 60.0
    target_width = 31.0
    target_height = 48.0

    accuracy_l = 100 * (1 - abs(length - target_length) / target_length)
    accuracy_w = 100 * (1 - abs(width - target_width) / target_width)
    accuracy_h = 100 * (1 - abs(height - target_height) / target_height)

    print(f"Accuracy: L:{accuracy_l:.2f}%, W:{accuracy_w:.2f}%, H:{accuracy_h:.2f}%")

    if accuracy_l >= 99.5 and accuracy_w >= 99.5 and accuracy_h >= 99.5:
        print("Model satisfies the 99.5% accuracy requirement.")
        return True
    else:
        print("Model DOES NOT satisfy the 99.5% accuracy requirement.")
        return False

if __name__ == "__main__":
    verify_benchy()
