import sys
import os

# Setup FreeCAD path
def setup_freecad():
    paths = [
        os.environ.get("FREECADPATH"),
        "/usr/lib/freecad-python3/lib",
        "/usr/lib/freecad/lib",
        "/usr/local/lib/freecad/lib"
    ]
    for p in paths:
        if p and os.path.exists(p):
            if p not in sys.path:
                sys.path.append(p)
            return True
    return False

setup_freecad()

import FreeCAD as App

def verify_benchy():
    print("Verifying Benchy...")

    fcstd_path = "output/benchy.FCStd"
    if not os.path.exists(fcstd_path):
        fcstd_path = "benchy.FCStd" # Check root too

    if not os.path.exists(fcstd_path):
        print(f"FAILED: benchy.FCStd not found.")
        return False

    doc = App.openDocument(fcstd_path)
    obj = doc.getObject("Benchy")
    bb = obj.Shape.BoundBox

    print(f"Bounding Box: X={bb.XLength:.2f}, Y={bb.YLength:.2f}, Z={bb.ZLength:.2f}")

    errors = []
    if not (59.0 <= bb.XLength <= 61.0):
        errors.append(f"X Length out of range: {bb.XLength}")
    if not (30.0 <= bb.YLength <= 32.0):
        errors.append(f"Y Length out of range: {bb.YLength}")
    if not (45.0 <= bb.ZLength <= 50.0):
        errors.append(f"Z Length out of range: {bb.ZLength}")

    # Check for PDF report
    if not os.path.exists("output/benchy_report.pdf") and not os.path.exists("benchy_report.pdf"):
        errors.append("PDF report missing.")

    if errors:
        for err in errors:
            print(f"ERROR: {err}")
        return False
    else:
        print("SUCCESS: Benchy meets specifications.")
        return True

if __name__ == "__main__":
    if verify_benchy():
        sys.exit(0)
    else:
        sys.exit(1)
