import sys
import os

# Set up FreeCAD paths
sys.path.append(os.path.abspath('tools'))
import freecad_utils
if not freecad_utils.setup_freecad():
    print("Error: Could not find FreeCAD library.")
    sys.exit(1)

import FreeCAD
import Part
import math

def create_benchy():
    doc = FreeCAD.newDocument("Benchy")

    # 1. Hull
    # Dimensions: L=60, W=31, H=15
    # Simplified hull using a wedge or modified box
    hull_base = Part.makeBox(60, 31, 15, FreeCAD.Vector(-30, -15.5, 0))

    # Shape the bow (40 degree overhang)
    # Bow is at +30. We cut with a plane.
    # z=15 at x=30, z=0 at x=30 - 15*tan(40)
    bow_cut_dist = 15 * math.tan(math.radians(40))
    bow_plane_point = FreeCAD.Vector(30 - bow_cut_dist, -16, 0)
    bow_plane_normal = FreeCAD.Vector(15, 0, -bow_cut_dist) # Approximately 40 deg
    # For simplicity, let's use a box and cut it.
    bow_cutter = Part.makeBox(40, 40, 40, FreeCAD.Vector(30 - bow_cut_dist, -20, 0))
    # Rotate cutter to create the 40 deg angle
    bow_cutter.rotate(FreeCAD.Vector(30 - bow_cut_dist, 0, 0), FreeCAD.Vector(0, 1, 0), -40)
    hull = hull_base.cut(bow_cutter)

    # Shape the sides (approximate the boat curve)
    side_cutter_l = Part.makeCylinder(50, 60, FreeCAD.Vector(0, 50 + 15.5 - 5, 0))
    side_cutter_r = Part.makeCylinder(50, 60, FreeCAD.Vector(0, -(50 + 15.5 - 5), 0))
    hull = hull.cut(side_cutter_l).cut(side_cutter_r)

    # 2. Deck
    # Slightly smaller box on top of the hull base
    deck = Part.makeBox(50, 26, 2, FreeCAD.Vector(-28, -13, 13))
    hull = hull.fuse(deck)

    # 3. Cabin
    # L=25, W=20, H=20 starting at Z=15
    cabin_outer = Part.makeBox(25, 20, 20, FreeCAD.Vector(-15, -10, 15))
    # Hollow out the cabin
    cabin_inner = Part.makeBox(21, 16, 18, FreeCAD.Vector(-13, -8, 15))
    cabin = cabin_outer.cut(cabin_inner)

    # Windows
    # Front window
    win_front = Part.makeBox(2, 10, 8, FreeCAD.Vector(8, -5, 23))
    # Side windows
    win_side_l = Part.makeBox(10, 2, 8, FreeCAD.Vector(-5, 8, 23))
    win_side_r = Part.makeBox(10, 2, 8, FreeCAD.Vector(-5, -10, 23))
    cabin = cabin.cut(win_front).cut(win_side_l).cut(win_side_r)

    # Roof (5.5 degree inclination)
    roof = Part.makeBox(30, 24, 2, FreeCAD.Vector(-18, -12, 35))
    roof.rotate(FreeCAD.Vector(-18, 0, 35), FreeCAD.Vector(0, 1, 0), -5.5)
    cabin = cabin.fuse(roof)

    # 4. Chimney
    # Cylindrical, hollow
    # To reach H=48, start at Z=35 and height=13
    chimney_outer = Part.makeCylinder(3.5, 13, FreeCAD.Vector(2, 0, 35))
    chimney_inner = Part.makeCylinder(2.5, 14, FreeCAD.Vector(2, 0, 35))
    chimney = chimney_outer.cut(chimney_inner)

    # Combine everything
    benchy_shape = hull.fuse(cabin).fuse(chimney)

    # Final Object
    final_obj = doc.addObject("Part::Feature", "BenchyModel")
    final_obj.Shape = benchy_shape

    doc.recompute()

    # Save
    os.makedirs('output', exist_ok=True)
    doc.saveAs("output/benchy.fcstd")
    benchy_shape.exportStl("output/benchy.stl")

    print("Benchy generated at output/benchy.fcstd and output/benchy.stl")
    return doc, final_obj

if __name__ == "__main__":
    create_benchy()
