import sys
import os
import math

# Add FreeCAD to path
from freecad_utils import setup_freecad
if not setup_freecad():
    print("FreeCAD not found. Please check your installation.")
    sys.exit(1)

import FreeCAD
import Part
import Mesh

def create_benchy():
    doc = FreeCAD.newDocument("Benchy")

    # Target: Length 60, Width 31, Height 48

    # 1. Hull
    wire1 = Part.makePolygon([
        FreeCAD.Vector(5, 0, 0),
        FreeCAD.Vector(40, 10, 0),
        FreeCAD.Vector(55, 0, 0),
        FreeCAD.Vector(40, -10, 0),
        FreeCAD.Vector(5, 0, 0)
    ])
    wire2 = Part.makePolygon([
        FreeCAD.Vector(0, 0, 15),
        FreeCAD.Vector(40, 15.5, 15),
        FreeCAD.Vector(60, 0, 15),
        FreeCAD.Vector(40, -15.5, 15),
        FreeCAD.Vector(0, 0, 15)
    ])
    hull_shell = Part.makeLoft([wire1, wire2], True)
    hull = doc.addObject("Part::Feature", "Hull")
    hull.Shape = hull_shell

    # 2. Deck
    deck_box = Part.makeBox(40, 26, 2, FreeCAD.Vector(10, -13, 13))
    deck = doc.addObject("Part::Feature", "Deck")
    deck.Shape = deck_box

    # 3. Cabin
    cabin_box = Part.makeBox(20, 20, 15, FreeCAD.Vector(15, -10, 15))

    # Roof inclination 5.5 degrees
    # Length 25, Width 24.
    # Height difference = tan(5.5) * 25 = 2.41 mm
    # Roof base at Z=30. We want top front at Z=37.
    # So roof height is 7.
    # makeWedge(xmin, ymin, zmin, x2min, z2min, xmax, ymax, zmax, x2max, z2max)
    # The signature in 0.21.2 seems to be:
    # xmin, ymin, zmin, x2min, z2min, xmax, ymax, zmax, x2max, z2max
    # Let's try to just use a box and rotate it for inclination.
    roof_box = Part.makeBox(25, 24, 2, FreeCAD.Vector(12.5, -12, 35))
    # Rotate 5.5 degrees around Y axis at the front edge
    roof_box.rotate(FreeCAD.Vector(12.5, 0, 37), FreeCAD.Vector(0, 1, 0), -5.5)

    cabin = doc.addObject("Part::Feature", "Cabin")
    cabin.Shape = cabin_box.fuse(roof_box)

    # 4. Chimney
    # Target height 48. Chimney height 11. 48 - 11 = 37.
    chimney_cyl = Part.makeCylinder(3.5, 11, FreeCAD.Vector(25, 0, 37), FreeCAD.Vector(0, 0, 1))
    chimney = doc.addObject("Part::Feature", "Chimney")
    chimney.Shape = chimney_cyl

    # 5. Fuse everything
    benchy_shape = hull.Shape.fuse(deck.Shape).fuse(cabin.Shape).fuse(chimney.Shape)
    benchy = doc.addObject("Part::Feature", "Benchy_Model")
    benchy.Shape = benchy_shape

    doc.recompute()

    bbox = benchy.Shape.BoundBox
    print(f"Internal BBox: L={bbox.XMax-bbox.XMin}, W={bbox.YMax-bbox.YMin}, H={bbox.ZMax-bbox.ZMin}")

    if not os.path.exists("output"):
        os.makedirs("output")

    doc.saveAs("output/benchy.FCStd")
    Mesh.export([benchy], "output/benchy.stl")

    print("Benchy model generated and exported to output/benchy.FCStd and output/benchy.stl")

if __name__ == "__main__":
    create_benchy()
