import sys
import os

def setup_freecad():
    # Potential paths for FreeCAD library
    potential_paths = [
        "/usr/lib/freecad-python3/lib",
        "/usr/lib/freecad/lib",
        "/usr/local/lib/freecad/lib",
    ]

    # Check environment variable if set
    if "FREECADPATH" in os.environ:
        potential_paths.insert(0, os.environ["FREECADPATH"])

    for path in potential_paths:
        if os.path.exists(path):
            if path not in sys.path:
                sys.path.append(path)
            try:
                import FreeCAD
                return True
            except ImportError:
                continue
    return False

def get_techdraw_template():
    # Standard location for TechDraw templates
    template_path = "/usr/share/freecad/Mod/TechDraw/Templates/A4_Landscape_TD.svg"
    if os.path.exists(template_path):
        return template_path
    return None
