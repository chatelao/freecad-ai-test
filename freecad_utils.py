import sys
import os

def setup_freecad():
    """Finds and adds FreeCAD to sys.path if not already present."""
    if 'FreeCAD' in sys.modules:
        return True

    potential_paths = [
        os.environ.get('FREECADPATH'),
        '/usr/lib/freecad-python3/lib',
        '/usr/lib/freecad/lib',
        '/usr/local/lib/freecad/lib'
    ]

    for path in potential_paths:
        if path and os.path.exists(os.path.join(path, 'FreeCAD.so')):
            if path not in sys.path:
                sys.path.append(path)
            try:
                import FreeCAD
                return True
            except ImportError:
                continue

    print("Error: Could not find FreeCAD library. Please set FREECADPATH environment variable.")
    return False

def get_template_path(template_name="A4_LandscapeTD.svg"):
    """Finds the TechDraw template path."""
    potential_dirs = [
        "/usr/share/freecad/Mod/TechDraw/Templates",
        "/usr/local/share/freecad/Mod/TechDraw/Templates"
    ]

    for d in potential_dirs:
        full_path = os.path.join(d, template_name)
        if os.path.exists(full_path):
            return full_path

    # Fallback if not found on disk, let FreeCAD try its search path
    return template_name
