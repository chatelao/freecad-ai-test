import sys
import os

def setup_freecad():
    # Potential FreeCAD paths
    FREECAD_PATHS = [
        '/usr/lib/freecad-python3/lib',
        '/usr/lib/freecad/lib',
        '/usr/local/lib/freecad/lib',
    ]

    # Check if FREECADPATH is in environment
    if 'FREECADPATH' in os.environ:
        FREECAD_PATHS.insert(0, os.environ['FREECADPATH'])

    for path in FREECAD_PATHS:
        if os.path.exists(path):
            if path not in sys.path:
                sys.path.append(path)
            try:
                import FreeCAD
                # Some modules might need to be imported differently or from specific paths
                return True
            except ImportError as e:
                print(f"Error importing FreeCAD from {path}: {e}")
                continue
    return False

if __name__ == "__main__":
    if setup_freecad():
        import FreeCAD
        print(f"FreeCAD found: {FreeCAD.Version()}")
    else:
        print("FreeCAD not found.")
        sys.exit(1)
