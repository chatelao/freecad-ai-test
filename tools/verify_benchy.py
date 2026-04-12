import sys
import os

# Add FreeCAD to path
from freecad_utils import setup_freecad
if not setup_freecad():
    print("FreeCAD not found.")
    sys.exit(1)

import Mesh

def verify_stl(filepath):
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found.")
        return False

    # Use Mesh.read instead of Mesh.Mesh to avoid potential segfaults in headless
    mesh = Mesh.read(filepath)
    bbox = mesh.BoundBox

    length = bbox.XMax - bbox.XMin
    width = bbox.YMax - bbox.YMin
    height = bbox.ZMax - bbox.ZMin

    print(f"STL Bounding Box: Length={length:.2f}, Width={width:.2f}, Height={height:.2f}")

    # Target: 60 x 31 x 48
    target_l, target_w, target_h = 60, 31, 48
    tolerance = 0.05 # 5% tolerance for initial model, though goal is 0.5%

    l_err = abs(length - target_l) / target_l
    w_err = abs(width - target_w) / target_w
    h_err = abs(height - target_h) / target_h

    print(f"Errors: L={l_err:.2%}, W={w_err:.2%}, H={h_err:.2%}")

    if l_err < 0.05 and w_err < 0.05 and h_err < 0.05:
        print("Verification PASSED (within 5% tolerance)")
        if l_err < 0.005 and w_err < 0.005 and h_err < 0.005:
            print("Verification EXCELLENT (within 0.5% tolerance)")
        return True
    else:
        print("Verification FAILED (outside 5% tolerance)")
        return False

if __name__ == "__main__":
    path = "output/benchy.stl"
    if len(sys.argv) > 1:
        path = sys.argv[1]

    if not verify_stl(path):
        sys.exit(1)
