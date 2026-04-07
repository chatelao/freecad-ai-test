import sys
import os

def find_freecad():
    # Common paths on Linux
    paths = [
        '/usr/lib/freecad-python3/lib',
        '/usr/lib/freecad/lib',
        '/usr/local/lib/freecad/lib'
    ]

    # Also check environment variable
    if 'FREECADPATH' in os.environ:
        paths.insert(0, os.environ['FREECADPATH'])

    for path in paths:
        if os.path.exists(os.path.join(path, 'FreeCAD.so')):
            return path
    return None

def test_imports():
    path = find_freecad()
    if not path:
        print("Error: FreeCAD library not found.")
        sys.exit(1)

    sys.path.append(path)

    try:
        import FreeCAD
        import Part
        import Mesh
        import _PartDesign as PartDesign
        print("FreeCAD environment test PASSED.")
        print(f"FreeCAD library path: {path}")
        print(f"FreeCAD version: {FreeCAD.Version()}")
        return True
    except ImportError as e:
        print(f"FreeCAD environment test FAILED: {e}")
        return False

if __name__ == "__main__":
    if test_imports():
        sys.exit(0)
    else:
        sys.exit(1)
