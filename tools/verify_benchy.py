import sys
import os
from freecad_utils import setup_freecad

FreeCAD, Part, Mesh, PartDesign = setup_freecad()

def verify_benchy():
    stl_path = "benchy.stl"
    if not os.path.exists(stl_path):
        print(f"Error: {stl_path} not found.")
        sys.exit(1)

    # Use Mesh.read instead of Mesh.Mesh to avoid potential segfaults in headless
    mesh = Mesh.read(stl_path)
    bbox = mesh.BoundBox

    print(f"Bounding Box dimensions:")
    print(f"Length (X): {bbox.XLength:.2f} mm")
    print(f"Width (Y): {bbox.YLength:.2f} mm")
    print(f"Height (Z): {bbox.ZLength:.2f} mm")

    # Target values
    targets = {
        "Length": (60.00, bbox.XLength),
        "Width": (31.00, bbox.YLength),
        "Height": (48.00, bbox.ZLength)
    }

    passed = True
    tolerance = 0.005 # 0.5%

    for name, (target, actual) in targets.items():
        diff = abs(target - actual)
        percent_diff = (diff / target)
        if percent_diff > tolerance:
            print(f"FAIL: {name} deviation too high: {percent_diff:.2%} (> {tolerance:.2%})")
            passed = False
        else:
            print(f"PASS: {name} deviation: {percent_diff:.2%} (within {tolerance:.2%})")

    if passed:
        print("Model dimensions are within 99.5% accuracy.")
    else:
        print("Model dimensions EXCEED tolerance.")
        sys.exit(1)

if __name__ == "__main__":
    verify_benchy()
