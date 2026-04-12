import sys
import os

def setup_freecad():
    # Common FreeCAD paths
    paths = [
        '/usr/lib/freecad-python3/lib',
        '/usr/lib/freecad/lib',
        '/usr/local/lib/freecad/lib'
    ]

    # Add FREECADPATH if set
    if 'FREECADPATH' in os.environ:
        paths.insert(0, os.environ['FREECADPATH'])

    for path in paths:
        if os.path.exists(path):
            if path not in sys.path:
                sys.path.append(path)
            try:
                import FreeCAD
                return True
            except ImportError:
                continue
    return False

if __name__ == "__main__":
    if setup_freecad():
        import FreeCAD
        print(f"FreeCAD {FreeCAD.Version()} successfully imported.")
    else:
        print("FreeCAD not found.")
        sys.exit(1)
