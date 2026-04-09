import os
import sys
from freecad_utils import setup_freecad

if not setup_freecad():
    print("Error: FreeCAD could not be loaded.")
    sys.exit(1)

import FreeCAD
import Mesh

def verify_stl(filepath):
    if not os.path.exists(filepath):
        print(f"File {filepath} not found.")
        return False

    try:
        # Since Mesh.read might segfault, we'll try to verify using FCStd if possible,
        # but the requirement says verify STL.
        # Let's try to use FreeCAD.openDocument and Mesh.insert which is sometimes safer.
        doc = FreeCAD.newDocument("Temp")
        Mesh.insert(filepath, doc.Name)
        m_obj = doc.ActiveObject
        bbox = m_obj.Mesh.BoundBox

        xl = bbox.XLength
        yl = bbox.YLength
        zl = bbox.ZLength

        print(f"Verification for {filepath}:")
        print(f"  Bounding Box: X={xl:.2f}, Y={yl:.2f}, Z={zl:.2f}")

        success = True
        if abs(xl - 60.0) > 0.3:
            print(f"  [FAIL] X Length {xl:.2f} is outside 99.5% tolerance of 60.0")
            success = False
        else:
            print(f"  [PASS] X Length {xl:.2f} is within tolerance.")

        if abs(yl - 31.0) > 0.155:
            print(f"  [FAIL] Y Width {yl:.2f} is outside 99.5% tolerance of 31.0")
            success = False
        else:
            print(f"  [PASS] Y Width {yl:.2f} is within tolerance.")

        if abs(zl - 48.0) > 0.24:
            print(f"  [FAIL] Z Height {zl:.2f} is outside 99.5% tolerance of 48.0")
            success = False
        else:
            print(f"  [PASS] Z Height {zl:.2f} is within tolerance.")

        FreeCAD.closeDocument(doc.Name)
        return success
    except Exception as e:
        print(f"Error verifying {filepath}: {e}")
        return False

if __name__ == "__main__":
    # Check both output and root for convenience
    paths = ["output/benchy.stl", "benchy.stl", "output/benchy_scad.stl", "benchy_scad.stl"]
    results = []
    for p in paths:
        if os.path.exists(p):
            results.append(verify_stl(p))

    if all(results) and len(results) >= 2:
        print("\nAll found models passed 99.5% accuracy check.")
        sys.exit(0)
    else:
        print("\nSome models failed or were not found.")
        sys.exit(1)
