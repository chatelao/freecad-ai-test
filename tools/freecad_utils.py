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
        if os.path.exists(path):
            if path not in sys.path:
                sys.path.append(path)
            return path
    return None

def get_freecad_bin():
    bins = [
        "/usr/lib/freecad/bin/freecad-python3",
        "/usr/lib/freecad/bin/freecadcmd-python3",
        "/usr/bin/freecadcmd",
    ]
    for b in bins:
        if os.path.exists(b):
            return b
    return "freecadcmd"

def get_techdraw_template_path():
    paths = [
        "/usr/share/freecad/Mod/TechDraw/Templates/A4_Landscape_TD.svg",
        "/usr/lib/freecad/Mod/TechDraw/Templates/A4_Landscape_TD.svg",
    ]
    for p in paths:
        if os.path.exists(p):
            return p
    return None
