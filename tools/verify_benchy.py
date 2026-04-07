import sys
import os

# Use the discovery utility to set up the FreeCAD environment.
# Since it's in the same 'tools' folder, we'll try to import it directly.
try:
    from freecad_utils import setup_freecad
    if not setup_freecad():
        print("FreeCAD environment setup failed.")
        sys.exit(1)
except ImportError:
    # If not in the same folder during execution, try adding the script's directory to sys.path.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(script_dir)
    from freecad_utils import setup_freecad
    if not setup_freecad():
         print("FreeCAD environment setup failed.")
         sys.exit(1)

import FreeCAD

def verify_benchy():
    output_dir = "output"
    fcstd_file = os.path.join(output_dir, "benchy.fcstd")

    if not os.path.exists(fcstd_file):
        print(f"Error: {fcstd_file} not found. Please run draw_benchy.py first.")
        sys.exit(1)

    doc = FreeCAD.open(fcstd_file)
    benchy_obj = doc.getObject("BenchyModel")

    if not benchy_obj:
        print("Error: BenchyModel object not found in document.")
        sys.exit(1)

    # Check bounding box
    bbox = benchy_obj.Shape.BoundBox
    print(f"Bounding Box dimensions: Length={bbox.XLength:.2f}, Width={bbox.YLength:.2f}, Height={bbox.ZLength:.2f}")

    # Expected dimensions (approximate)
    expected_length = 60.0
    expected_width = 31.0
    expected_height = 48.0

    # Tolerance for simplified model
    tolerance = 5.0

    passed = True
    if abs(bbox.XLength - expected_length) > tolerance:
        print(f"Warning: Length mismatch. Expected {expected_length}, got {bbox.XLength:.2f}")
        passed = False
    if abs(bbox.YLength - expected_width) > tolerance:
        print(f"Warning: Width mismatch. Expected {expected_width}, got {bbox.YLength:.2f}")
        passed = False
    if abs(bbox.ZLength - expected_height) > tolerance:
        print(f"Warning: Height mismatch. Expected {expected_height}, got {bbox.ZLength:.2f}")
        passed = False

    if passed:
        print("Verification: PASSED (within tolerance)")
    else:
        print("Verification: FAILED (outside tolerance)")

if __name__ == "__main__":
    verify_benchy()
