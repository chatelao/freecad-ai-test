import sys
import os

# Import setup_freecad from freecad_utils
sys.path.append(os.path.join(os.path.dirname(__file__)))
from freecad_utils import setup_freecad

if not setup_freecad():
    print("Failed to initialize FreeCAD. Exiting.")
    sys.exit(1)

import FreeCAD
import Part
import Mesh

def create_hull():
    """
    Creates a more realistic hull using lofted cross-sections.
    """
    # Stern at X=0, Bow at X=60
    # Bottom cross-section (flat, narrow)
    c1_pts = [FreeCAD.Vector(5, -5, 0), FreeCAD.Vector(50, 0, 0), FreeCAD.Vector(5, 5, 0), FreeCAD.Vector(5, -5, 0)]
    c1 = Part.Wire([Part.makeLine(c1_pts[i], c1_pts[i+1]) for i in range(3)])

    # Middle cross-section (wider)
    c2_pts = [FreeCAD.Vector(2, -15.0, 8), FreeCAD.Vector(55, 0, 8), FreeCAD.Vector(2, 15.0, 8), FreeCAD.Vector(2, -15.0, 8)]
    c2 = Part.Wire([Part.makeLine(c2_pts[i], c2_pts[i+1]) for i in range(3)])

    # Top cross-section (deck level)
    c3_pts = [FreeCAD.Vector(0, -15.5, 15.5), FreeCAD.Vector(60, 0, 15.5), FreeCAD.Vector(0, 15.5, 15.5), FreeCAD.Vector(0, -15.5, 15.5)]
    c3 = Part.Wire([Part.makeLine(c3_pts[i], c3_pts[i+1]) for i in range(3)])

    hull_solid = Part.makeLoft([c1, c2, c3], True)
    return hull_solid

def create_cabin(hull):
    """
    Creates the cabin (bridge) with windows and a slanted roof.
    """
    # Main cabin block
    cabin_base = Part.makeBox(22, 18, 20, FreeCAD.Vector(18, -9, 15.5))

    # Window cutouts
    front_window = Part.makeBox(5, 12, 10, FreeCAD.Vector(36, -6, 22))
    side_window_l = Part.makeBox(12, 5, 10, FreeCAD.Vector(23, -11, 22))
    side_window_r = Part.makeBox(12, 5, 10, FreeCAD.Vector(23, 6, 22))

    cabin = cabin_base.cut(front_window).cut(side_window_l).cut(side_window_r)

    # Slanted roof
    roof_pts = [
        FreeCAD.Vector(16, -11, 35.5),
        FreeCAD.Vector(42, -11, 33.5), # 2mm drop over 26mm is ~4.4 degrees
        FreeCAD.Vector(42, 11, 33.5),
        FreeCAD.Vector(16, 11, 35.5),
        FreeCAD.Vector(16, -11, 35.5)
    ]
    roof_wire = Part.Wire([Part.makeLine(roof_pts[i], roof_pts[i+1]) for i in range(4)])
    roof_face = Part.Face(roof_wire)
    roof_solid = roof_face.extrude(FreeCAD.Vector(0, 0, 2))

    return cabin.fuse(roof_solid)

def create_chimney():
    """
    Creates the chimney.
    Dimensions: 7mm outer diameter, 11mm height.
    """
    # Chimney on top of the roof (approx. X=30)
    chimney_outer = Part.makeCylinder(3.5, 11, FreeCAD.Vector(28, 0, 37.5))
    chimney_inner = Part.makeCylinder(1.5, 12, FreeCAD.Vector(28, 0, 37.5))

    return chimney_outer.cut(chimney_inner)

def main():
    # Create a new document
    doc = FreeCAD.newDocument("Benchy")

    # Create the parts
    hull = create_hull()
    cabin = create_cabin(hull)
    chimney = create_chimney()

    # Fuse all parts
    benchy = hull.fuse(cabin).fuse(chimney)

    # Add to document
    part_obj = doc.addObject("Part::Feature", "Benchy")
    part_obj.Shape = benchy

    # Save document
    doc.saveAs("benchy.FCStd")

    # Export to STL
    Mesh.export([part_obj], "benchy.stl")

    print("Benchy model generated successfully.")

if __name__ == "__main__":
    main()
