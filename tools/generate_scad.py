import os
import sys

# Add the root directory to sys.path to find freecad_utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import freecad_utils

def generate_scad():
    FreeCAD = freecad_utils.init_freecad()
    # Need to add OpenSCAD mod path to sys.path which is done in setup_freecad_paths
    import exportCSG

    # Fix for FreeCAD 0.21 exportCSG bug mentioned in memory
    exportCSG.pythonopen = open

    doc = FreeCAD.open("output/benchy.FCStd")
    obj = doc.getObject("Benchy")

    output_scad = "output/benchy.scad"
    exportCSG.export([obj], output_scad)
    print(f"Exported {output_scad}")

if __name__ == "__main__":
    generate_scad()
