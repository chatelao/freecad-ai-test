import sys
import os
from freecad_utils import init_freecad

def verify_benchy():
    FreeCAD = init_freecad()
    if not FreeCAD:
        sys.exit(1)

    import Mesh

    stl_path = "output/benchy.stl"
    if not os.path.exists(stl_path):
        # check in root as well
        stl_path = "benchy.stl"
        if not os.path.exists(stl_path):
            print("STL file not found.")
            sys.exit(1)

    mesh = Mesh.Mesh(stl_path)
    bb = mesh.BoundBox

    print(f"Bounding Box: {bb.XLength:.2f} x {bb.YLength:.2f} x {bb.ZLength:.2f}")

    # Expected: 60x31x48
    expected_x = 60.0
    expected_y = 31.0
    expected_z = 48.0

    tol = 0.1

    if abs(bb.XLength - expected_x) < tol and \
       abs(bb.YLength - expected_y) < tol and \
       abs(bb.ZLength - expected_z) < tol:
        print("Verification PASSED: Dimensions match standard Benchy.")
    else:
        print("Verification FAILED: Dimensions do not match.")

if __name__ == "__main__":
    verify_benchy()
