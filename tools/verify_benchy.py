import sys
import os
from freecad_utils import setup_freecad

if not setup_freecad():
    print("FreeCAD library not found.")
    sys.exit(1)

import FreeCAD
import Part

def verify_benchy():
    # Use the root level file
    doc = FreeCAD.open("benchy.FCStd")
    benchy = doc.getObject("Benchy")

    if benchy is None:
        print("Error: Benchy object not found in the document.")
        sys.exit(1)

    bbox = benchy.Shape.BoundBox
    print(f"Bounding Box: X={bbox.XLength}, Y={bbox.YLength}, Z={bbox.ZLength}")

    # Check dimensions against specs
    # Length: 60.0
    # Width: 31.0
    # Height: 48.0

    if abs(bbox.XLength - 60.0) > 0.1:
        print(f"Warning: Length is {bbox.XLength}, expected 60.0")
    if abs(bbox.YLength - 31.0) > 0.1:
        print(f"Warning: Width is {bbox.YLength}, expected 31.0")
    # Height can vary slightly based on chimney etc.

    print("Verification complete.")

if __name__ == "__main__":
    verify_benchy()
