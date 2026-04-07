import sys
import os
from freecad_utils import setup_freecad

if not setup_freecad():
    print("FreeCAD library not found.")
    sys.exit(1)

import FreeCAD
import Part
import math

def draw_benchy():
    doc = FreeCAD.newDocument("Benchy")

    # Constants
    LENGTH = 60.0
    WIDTH = 31.0
    HEIGHT = 48.0
    DECK_HEIGHT = 15.5

    # 1. Hull
    # Base block
    hull_main = Part.makeBox(LENGTH - 20, WIDTH, DECK_HEIGHT)
    hull_main.translate(FreeCAD.Vector(0, -WIDTH/2, 0))

    # Simple bow using wedge
    # xmin, ymin, zmin, x2min, y2min, xmax, ymax, zmax, x2max, y2max
    bow_wedge = Part.makeWedge(LENGTH-20, -WIDTH/2, 0, LENGTH-20, 0, LENGTH, WIDTH/2, DECK_HEIGHT, LENGTH, 0)

    hull = hull_main.fuse(bow_wedge)

    # 2. Cabin
    cabin_len = 23.0
    cabin_width = 25.0
    cabin_height = 18.0
    cabin = Part.makeBox(cabin_len, cabin_width, cabin_height)
    cabin.translate(FreeCAD.Vector(15, -cabin_width/2, DECK_HEIGHT))

    # Windows
    # Front window: 10.5 x 9.5
    front_win = Part.makeBox(5, 10.5, 9.5)
    front_win.translate(FreeCAD.Vector(15 - 2, -10.5/2, DECK_HEIGHT + 5))
    cabin = cabin.cut(front_win)

    # Side windows
    side_win_l = 10
    side_win_w = 5
    side_win_h = 8
    side_win = Part.makeBox(side_win_l, side_win_w, side_win_h)
    side_win.translate(FreeCAD.Vector(15 + 6, -cabin_width/2 - 2, DECK_HEIGHT + 6))
    cabin = cabin.cut(side_win)
    side_win_2 = Part.makeBox(side_win_l, side_win_w, side_win_h)
    side_win_2.translate(FreeCAD.Vector(15 + 6, cabin_width/2 - 3, DECK_HEIGHT + 6))
    cabin = cabin.cut(side_win_2)

    # Rear window (circular)
    rear_win = Part.makeCylinder(4.5, 10) # Diameter 9
    rear_win.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,1,0), 90)
    rear_win.translate(FreeCAD.Vector(15 + cabin_len - 5, 0, DECK_HEIGHT + 10))
    cabin = cabin.cut(rear_win)

    # 3. Roof
    roof_inclination = 5.5
    roof_len = 28.0
    roof_width = 28.0
    roof_thick = 2.0
    roof = Part.makeBox(roof_len, roof_width, roof_thick)
    roof.translate(FreeCAD.Vector(12, -roof_width/2, DECK_HEIGHT + cabin_height))
    # Tilting the roof
    roof.rotate(FreeCAD.Vector(12 + roof_len, 0, DECK_HEIGHT + cabin_height), FreeCAD.Vector(0, 1, 0), -roof_inclination)

    # 4. Chimney
    chim_h = 12.0
    chimney = Part.makeCylinder(3.5, chim_h)
    chimney_hole = Part.makeCylinder(1.5, chim_h + 2)
    chimney = chimney.cut(chimney_hole)
    chimney.translate(FreeCAD.Vector(15 + cabin_len/2 + 2, 0, DECK_HEIGHT + cabin_height))

    # 5. Cargo Box
    box_out_l = 12.0
    box_out_w = 10.81
    box_in_l = 8.0
    box_in_w = 7.0
    box_depth = 9.0
    box_h = 10.0

    cargo_box_out = Part.makeBox(box_out_l, box_out_w, box_h)
    cargo_box_out.translate(FreeCAD.Vector(2, -box_out_w/2, DECK_HEIGHT))
    cargo_box_in = Part.makeBox(box_in_l, box_in_w, box_depth + 1)
    cargo_box_in.translate(FreeCAD.Vector(2 + (box_out_l-box_in_l)/2, -box_in_w/2, DECK_HEIGHT + box_h - box_depth))
    cargo_box = cargo_box_out.cut(cargo_box_in)

    # Combine all
    # hull.fuse(cabin) etc.
    all_parts = [hull, cabin, roof, chimney, cargo_box]
    benchy_shape = all_parts[0]
    for p in all_parts[1:]:
        benchy_shape = benchy_shape.fuse(p)

    # Export
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    benchy_shape.exportStl(os.path.join(output_dir, "benchy.stl"))
    obj = doc.addObject("Part::Feature", "Benchy")
    obj.Shape = benchy_shape

    # Save the document
    doc.recompute()
    doc.saveAs(os.path.join(output_dir, "benchy.FCStd"))
    print("Refined Benchy generated.")

if __name__ == "__main__":
    draw_benchy()
