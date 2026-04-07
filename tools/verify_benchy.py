import sys
import os
from freecad_utils import setup_freecad_path

# Setup FreeCAD path
setup_freecad_path()
import FreeCAD
import Mesh

def verify_benchy():
    stl_path = "output/benchy.stl"
    if not os.path.exists(stl_path):
        stl_path = "benchy.stl"

    if not os.path.exists(stl_path):
        print(f"Error: STL file not found at {stl_path}")
        return False

    try:
        # Mesh.Mesh(path) might cause SegFault in some environments, try Mesh.read()
        mesh = Mesh.read(stl_path)
        bb = mesh.BoundBox

        print(f"STL Bounding Box:")
        print(f"X: {bb.XMin:.2f} to {bb.XMax:.2f} (Length: {bb.XLength:.2f})")
        print(f"Y: {bb.YMin:.2f} to {bb.YMax:.2f} (Width: {bb.YLength:.2f})")
        print(f"Z: {bb.ZMin:.2f} to {bb.ZMax:.2f} (Height: {bb.ZLength:.2f})")

        valid = True
        if not (50 < bb.XLength < 70):
            print("X Length out of range.")
            valid = False
        if not (25 < bb.YLength < 40):
            print("Y Width out of range.")
            valid = False
        if not (40 < bb.ZLength < 55):
            print("Z Height out of range.")
            valid = False

        if valid:
            print("Verification PASSED")
        else:
            print("Verification FAILED")
        return valid
    except Exception as e:
        print(f"Verification encountered error: {e}")
        return False

if __name__ == "__main__":
    verify_benchy()
