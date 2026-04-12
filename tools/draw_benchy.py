import os
import sys
import math

# Setup FreeCAD path
from freecad_utils import setup_freecad, ensure_output_dir
if not setup_freecad():
    sys.exit(1)

import FreeCAD
import Part
import Mesh

def create_hull():
    """Creates the Benchy hull with 40 deg bow overhang."""
    # Profile 1: Bottom
    p1 = [
        FreeCAD.Vector(-20, 0, 0),
        FreeCAD.Vector(15, 7, 0),
        FreeCAD.Vector(28, 0, 0),
        FreeCAD.Vector(15, -7, 0),
        FreeCAD.Vector(-20, 0, 0)
    ]
    # Profile 2: Middle
    p2 = [
        FreeCAD.Vector(-25, 0, 10),
        FreeCAD.Vector(15, 15.2, 10),
        FreeCAD.Vector(30, 0, 10),
        FreeCAD.Vector(15, -15.2, 10),
        FreeCAD.Vector(-25, 0, 10)
    ]
    # Profile 3: Top
    # Bow overhang 40 deg. z=15. From bottom p1 back (-20,0,0) to top p3 back.
    # tan(40) = offset / 15 -> offset = 15 * tan(40) ~ 12.58
    p3 = [
        FreeCAD.Vector(-17.3 - 15*math.tan(math.radians(40)), 0, 15),
        FreeCAD.Vector(10, 15.05, 15),
        FreeCAD.Vector(30, 0, 15),
        FreeCAD.Vector(10, -15.05, 15),
        FreeCAD.Vector(-17.3 - 15*math.tan(math.radians(40)), 0, 15)
    ]

    w1 = Part.makePolygon(p1)
    w2 = Part.makePolygon(p2)
    w3 = Part.makePolygon(p3)

    hull = Part.makeLoft([w1, w2, w3], True)
    return hull

def create_deck():
    """Creates the deck."""
    deck = Part.makeBox(35, 28, 2, FreeCAD.Vector(-15, -14, 15))
    return deck

def create_cabin():
    """Creates the cabin with 5.5 deg roof inclination."""
    cabin_base = Part.makeBox(20, 20, 20, FreeCAD.Vector(-10, -10, 17))
    # Cut out the inside
    inner = Part.makeBox(18, 18, 20, FreeCAD.Vector(-9, -9, 18))
    cabin = cabin_base.cut(inner)

    # Roof with inclination
    # Tilt 5.5 deg around Y axis
    roof = Part.makeBox(22, 22, 2, FreeCAD.Vector(-11, -11, 0))
    roof.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,1,0), 5.5)
    roof.translate(FreeCAD.Vector(0, 0, 37))

    return cabin.fuse(roof)

def create_chimney():
    """Creates the chimney."""
    chimney = Part.makeCylinder(3, 9, FreeCAD.Vector(0, 0, 39))
    return chimney

def main():
    ensure_output_dir()
    doc = FreeCAD.newDocument("Benchy")

    hull = create_hull()
    deck = create_deck()
    cabin = create_cabin()
    chimney = create_chimney()

    # Combine parts
    benchy = hull.fuse(deck).fuse(cabin).fuse(chimney)

    # Center the model
    bbox = benchy.BoundBox
    center = bbox.Center
    benchy.translate(FreeCAD.Vector(-center.x, -center.y, -bbox.ZMin))

    # Add to document
    obj = doc.addObject("Part::Feature", "Benchy")
    obj.Shape = benchy

    # Save files
    doc.saveAs("output/benchy.FCStd")
    Mesh.export([obj], "output/benchy.stl")
    print("FreeCAD Benchy model generated in output/")

if __name__ == "__main__":
    main()
