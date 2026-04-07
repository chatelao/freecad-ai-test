import sys
import os

def setup_freecad():
    # Common paths for FreeCAD on Ubuntu
    possible_paths = [
        '/usr/lib/freecad-python3/lib',
        '/usr/lib/freecad/lib',
        '/usr/local/lib/freecad/lib'
    ]

    # Check if FREECADPATH is in environment
    if 'FREECADPATH' in os.environ:
        possible_paths.insert(0, os.environ['FREECADPATH'])

    for path in possible_paths:
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
    template_path = "/usr/share/freecad/Mod/TechDraw/Templates/A4_LandscapeTD.svg"
    if os.path.exists(template_path):
        return template_path
    # Fallback or search
    return None
