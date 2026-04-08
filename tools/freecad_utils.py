import sys
import os

# FreeCAD path discovery
FREECAD_PATHS = [
    "/usr/lib/freecad-python3/lib",
    "/usr/lib/freecad/lib",
    "/usr/local/lib/freecad/lib",
]

def setup_freecad():
    for path in FREECAD_PATHS:
        if os.path.exists(path) and path not in sys.path:
            sys.path.append(path)
            try:
                import FreeCAD
                return True
            except ImportError:
                continue
    return False

if not setup_freecad():
    print("Warning: FreeCAD not found in standard paths.")

import FreeCAD
import Part
import Mesh

def export_stl(objects, filename):
    Mesh.export(objects, filename)

def save_fcstd(doc, filename):
    doc.saveAs(filename)
