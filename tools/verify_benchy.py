import sys
import os

from freecad_utils import setup_freecad
setup_freecad()

import FreeCAD as App
import Part
import Mesh

def verify_benchy(filepath):
    print(f"Verifying {filepath}...")

    if filepath.endswith(".stl"):
        # Use Mesh.read to avoid segfaults in headless as per memory
        mesh = Mesh.read(filepath)
        bbox = mesh.BoundBox
    elif filepath.endswith(".FCStd"):
        doc = App.open(filepath)
        obj = doc.ActiveObject
        bbox = obj.Shape.BoundBox
    else:
        print("Unknown file format.")
        return False

    length = bbox.XMax - bbox.XMin
    width = bbox.YMax - bbox.YMin
    height = bbox.ZMax - bbox.ZMin

    print(f"Dimensions: {length:.2f} x {width:.2f} x {height:.2f}")

    target_l, target_w, target_h = 60.0, 31.0, 48.0

    acc_l = 100 * (1 - abs(length - target_l) / target_l)
    acc_w = 100 * (1 - abs(width - target_w) / target_w)
    acc_h = 100 * (1 - abs(height - target_h) / target_h)

    print(f"Accuracy: L:{acc_l:.2f}%, W:{acc_w:.2f}%, H:{acc_h:.2f}%")

    if acc_l >= 99.5 and acc_w >= 99.5 and acc_h >= 99.5:
        print("Verification PASSED!")
        return True
    else:
        print("Verification FAILED!")
        return False

if __name__ == "__main__":
    stl_path = "output/benchy.stl"
    if not os.path.exists(stl_path):
        stl_path = "benchy.stl"

    if os.path.exists(stl_path):
        verify_benchy(stl_path)
    else:
        print(f"File not found: {stl_path}")
        sys.exit(1)
