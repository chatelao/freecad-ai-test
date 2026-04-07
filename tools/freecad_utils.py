import sys
import os

def setup_freecad_path():
    paths = [
        "/usr/lib/freecad-python3/lib",
        "/usr/lib/freecad/lib",
        "/usr/local/lib/freecad/lib",
    ]
    if "FREECADPATH" in os.environ:
        paths.insert(0, os.environ["FREECADPATH"])

    for path in paths:
        if os.path.exists(os.path.join(path, "FreeCAD.so")) or os.path.exists(os.path.join(path, "FreeCAD.pyd")):
            sys.path.append(path)
            return path

    raise ImportError("FreeCAD library not found in standard paths.")

def get_techdraw_template_path():
    standard_path = "/usr/share/freecad/Mod/TechDraw/Templates/A4_Landscape_ISO7200TD.svg"
    if os.path.exists(standard_path):
        return standard_path
    # Fallback or search
    return None
