import sys
import os

sys.path.append(os.path.dirname(__file__))
import freecad_utils

if not freecad_utils.setup_freecad():
    sys.exit(1)

import FreeCAD
import Mesh

def verify_stl(stl_path):
    print(f"Verifying {stl_path}...")
    if not os.path.exists(stl_path):
        print("Error: STL file not found.")
        return False

    mesh = Mesh.read(stl_path)
    bbox = mesh.BoundBox

    length = bbox.XMax - bbox.XMin
    width = bbox.YMax - bbox.YMin
    height = bbox.ZMax - bbox.ZMin

    print(f"Dimensions: Length={length:.2f}, Width={width:.2f}, Height={height:.2f}")

    # Target Dimensions
    target_l, target_w, target_h = 60.0, 31.0, 48.0

    accuracy_l = (1 - abs(length - target_l) / target_l) * 100
    accuracy_w = (1 - abs(width - target_w) / target_w) * 100
    accuracy_h = (1 - abs(height - target_h) / target_h) * 100

    print(f"Accuracy: L={accuracy_l:.2f}%, W={accuracy_w:.2f}%, H={accuracy_h:.2f}%")

    if accuracy_l >= 99.5 and accuracy_w >= 99.5 and accuracy_h >= 99.5:
        print("Verification PASSED")
        return True
    else:
        print("Verification FAILED (Accuracy below 99.5%)")
        return False

if __name__ == "__main__":
    stl_path = "output/benchy_temp.stl"
    if len(sys.argv) > 1:
        stl_path = sys.argv[1]
    verify_stl(stl_path)
