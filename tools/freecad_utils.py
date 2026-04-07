import sys
import os

def setup_freecad_path():
    """
    Finds the FreeCAD library path and adds it to sys.path.
    """
    possible_paths = [
        '/usr/lib/freecad-python3/lib',
        '/usr/lib/freecad/lib',
        '/usr/local/lib/freecad/lib'
    ]

    # Check if FREECADPATH is set in environment
    if 'FREECADPATH' in os.environ:
        possible_paths.insert(0, os.environ['FREECADPATH'])

    for path in possible_paths:
        if os.path.exists(os.path.join(path, 'FreeCAD.so')):
            sys.path.append(path)
            return path

    # Fallback: try to find it using 'find' if the above fails (slower)
    return None

def init_freecad():
    path = setup_freecad_path()
    if path:
        try:
            import FreeCAD
            return FreeCAD
        except ImportError:
            print(f"Error: Could not import FreeCAD from {path}")
            return None
    else:
        print("Error: Could not find FreeCAD library.")
        return None
