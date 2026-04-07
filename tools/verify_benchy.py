import sys
import os

# Set up FreeCAD paths
sys.path.append(os.path.abspath('tools'))
import freecad_utils
if not freecad_utils.setup_freecad():
    print("Error: Could not find FreeCAD library.")
    sys.exit(1)

import FreeCAD

def verify_benchy():
    # 1. Check for expected files
    expected_files = [
        "output/benchy.fcstd",
        "output/benchy.stl",
        "output/report.pdf",
        "output/side_view.svg",
        "output/side_view.dxf"
    ]

    missing_files = [f for f in expected_files if not os.path.exists(f)]
    if missing_files:
        print(f"Error: Missing files: {missing_files}")
        return False
    else:
        print("All expected output files exist.")

    # 2. Check 3D model dimensions
    doc = FreeCAD.open("output/benchy.fcstd")
    benchy_model = doc.getObject("BenchyModel")
    if not benchy_model:
        print("Error: BenchyModel object not found in document.")
        return False

    bbox = benchy_model.Shape.BoundBox
    # Expected: 60x31x48
    # We use some tolerance
    tol = 1.0 # 1mm tolerance

    length = bbox.XMax - bbox.XMin
    width = bbox.YMax - bbox.YMin
    height = bbox.ZMax - bbox.ZMin

    print(f"Dimensions: L={length:.2f}, W={width:.2f}, H={height:.2f}")

    passed = True
    if abs(length - 60) > tol:
        print(f"Warning: Length {length:.2f} deviates from 60mm.")
        passed = False
    if abs(width - 31) > tol:
        print(f"Warning: Width {width:.2f} deviates from 31mm.")
        passed = False
    if abs(height - 48) > tol:
        print(f"Warning: Height {height:.2f} deviates from 48mm.")
        passed = False

    if passed:
        print("Model dimensions are within tolerance.")
    else:
        print("Model dimensions are OUTSIDE tolerance.")

    return passed

if __name__ == "__main__":
    if verify_benchy():
        print("Verification PASSED")
        sys.exit(0)
    else:
        print("Verification FAILED")
        sys.exit(1)
