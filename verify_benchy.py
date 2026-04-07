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

FREECADPATH = find_freecad()
if not FREECADPATH:
    print("Error: Could not find FreeCAD library.")
    sys.exit(1)

sys.path.append(FREECADPATH)

try:
    import FreeCAD
    import Part
    import Mesh
except ImportError as e:
    print(f"Error: {e}")
    sys.exit(1)

def verify_shape(shape, filename):
    try:
        bbox = shape.BoundBox
        print(f"File: {filename}")
        print(f"Bounding Box: {bbox}")
        print(f"X range: {bbox.XMax - bbox.XMin:.2f} mm")
        print(f"Y range: {bbox.YMax - bbox.YMin:.2f} mm")
        print(f"Z range: {bbox.ZMax - bbox.ZMin:.2f} mm")

        # Expected: X~60, Y~31, Z~48 (some variance is expected due to simplified model)
        expected_x = 60.0
        expected_y = 31.0
        expected_z = 48.0

        actual_x = bbox.XMax - bbox.XMin
        actual_y = bbox.YMax - bbox.YMin
        actual_z = bbox.ZMax - bbox.ZMin

        print("\nVerification against specifications:")
        print(f"X: {actual_x:.2f} (Expected {expected_x}) - Diff: {abs(actual_x - expected_x):.2f}")
        print(f"Y: {actual_y:.2f} (Expected {expected_y}) - Diff: {abs(actual_y - expected_y):.2f}")
        print(f"Z: {actual_z:.2f} (Expected {expected_z}) - Diff: {abs(actual_z - expected_z):.2f}")

    except Exception as e:
        print(f"Error reading STL: {e}")

if __name__ == "__main__":
    # We should also verify the Shape directly from draw_benchy if possible
    # or just trust the STL bbox if it represents everything.
    # The Mesh bbox in FreeCAD might be just for the mesh data.
    # Let's try to load the STL as a shape.
    try:
        mesh = Mesh.Mesh("benchy.stl")
        # Mesh BoundBox should be accurate.
        bbox = mesh.BoundBox
        print(f"File: benchy.stl")
        print(f"Bounding Box: {bbox}")
        print(f"X range: {bbox.XMax - bbox.XMin:.2f} mm")
        print(f"Y range: {bbox.YMax - bbox.YMin:.2f} mm")
        print(f"Z range: {bbox.ZMax - bbox.ZMin:.2f} mm")

        expected_x = 60.0
        expected_y = 31.0
        expected_z = 48.0

        actual_x = bbox.XMax - bbox.XMin
        actual_y = bbox.YMax - bbox.YMin
        actual_z = bbox.ZMax - bbox.ZMin

        print("\nVerification against specifications:")
        print(f"X: {actual_x:.2f} (Expected {expected_x}) - Diff: {abs(actual_x - expected_x):.2f}")
        print(f"Y: {actual_y:.2f} (Expected {expected_y}) - Diff: {abs(actual_y - expected_y):.2f}")
        print(f"Z: {actual_z:.2f} (Expected {expected_z}) - Diff: {abs(actual_z - expected_z):.2f}")
    except Exception as e:
        print(f"Error: {e}")
