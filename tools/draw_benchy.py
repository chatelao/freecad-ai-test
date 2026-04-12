import sys
import os

# Import utility
from freecad_utils import setup_freecad, export_stl, save_fcstd

if not setup_freecad():
    print("FreeCAD not found. Exiting.")
    sys.exit(1)

import FreeCAD
import Part
import math

def create_benchy():
    doc = FreeCAD.newDocument("Benchy")

    # Dimensions from benchy_specs.md
    LENGTH = 60.0
    WIDTH = 31.0
    HEIGHT = 48.0
    BOX_HEIGHT_ABOVE_BOTTOM = 15.5

    # --- Hull ---
    # Using a Loft for a more boat-like hull
    # Profile 1: Bottom (flat)
    p1 = Part.makePolygon([
        FreeCAD.Base.Vector(-20, -10, 0),
        FreeCAD.Base.Vector(20, -10, 0),
        FreeCAD.Base.Vector(30, 0, 0),
        FreeCAD.Base.Vector(20, 10, 0),
        FreeCAD.Base.Vector(-20, 10, 0),
        FreeCAD.Base.Vector(-20, -10, 0)
    ])

    # Profile 2: Deck level
    p2 = Part.makePolygon([
        FreeCAD.Base.Vector(-30, -WIDTH/2, BOX_HEIGHT_ABOVE_BOTTOM),
        FreeCAD.Base.Vector(10, -WIDTH/2, BOX_HEIGHT_ABOVE_BOTTOM),
        FreeCAD.Base.Vector(30, 0, BOX_HEIGHT_ABOVE_BOTTOM),
        FreeCAD.Base.Vector(10, WIDTH/2, BOX_HEIGHT_ABOVE_BOTTOM),
        FreeCAD.Base.Vector(-30, WIDTH/2, BOX_HEIGHT_ABOVE_BOTTOM),
        FreeCAD.Base.Vector(-30, -WIDTH/2, BOX_HEIGHT_ABOVE_BOTTOM)
    ])

    hull_loft = Part.makeLoft([p1, p2], True)

    # --- Deck & Cargo Box ---
    box_outer_w = 10.81
    box_outer_l = 12.0
    box_inner_w = 7.0
    box_inner_l = 8.0
    box_depth = 9.0

    cargo_box_outer = Part.makeBox(box_outer_l, box_outer_w, box_depth)
    cargo_box_outer.translate(FreeCAD.Base.Vector(-25, -box_outer_w/2, BOX_HEIGHT_ABOVE_BOTTOM))

    cargo_box_inner = Part.makeBox(box_inner_l, box_inner_w, box_depth + 1)
    cargo_box_inner.translate(FreeCAD.Base.Vector(-25 + (box_outer_l - box_inner_l)/2, -box_inner_w/2, BOX_HEIGHT_ABOVE_BOTTOM + (box_depth - 8)))

    cargo_box = cargo_box_outer.cut(cargo_box_inner)
    hull = hull_loft.fuse(cargo_box)

    # --- Bridge ---
    bridge_l = 23.0
    bridge_w = 23.0
    bridge_h = 20.0
    bridge = Part.makeBox(bridge_l, bridge_w, bridge_h)
    bridge.translate(FreeCAD.Base.Vector(-5, -bridge_w/2, BOX_HEIGHT_ABOVE_BOTTOM))

    # Windows
    front_win_w = 10.5
    front_win_h = 9.5
    front_win = Part.makeBox(2, front_win_w, front_win_h)
    front_win.translate(FreeCAD.Base.Vector(18-2, -front_win_w/2, BOX_HEIGHT_ABOVE_BOTTOM + 5))
    bridge = bridge.cut(front_win)

    # Rear window
    rear_win_r = 4.5
    rear_win = Part.makeCylinder(rear_win_r, 5)
    rear_win.rotate(FreeCAD.Base.Vector(0,0,0), FreeCAD.Base.Vector(0,1,0), 90)
    rear_win.translate(FreeCAD.Base.Vector(-5-1, 0, BOX_HEIGHT_ABOVE_BOTTOM + 10))
    bridge = bridge.cut(rear_win)

    # Roof
    roof_h = 2.0
    roof = Part.makeBox(bridge_l + 4, bridge_w + 2, roof_h)
    roof.translate(FreeCAD.Base.Vector(-7, -(bridge_w+2)/2, BOX_HEIGHT_ABOVE_BOTTOM + bridge_h))

    hull = hull.fuse(bridge)
    hull = hull.fuse(roof)

    # --- Chimney ---
    chimney_od = 7.0
    chimney_id = 3.0
    chimney_h = 48.0 - (BOX_HEIGHT_ABOVE_BOTTOM + bridge_h)
    chimney = Part.makeCylinder(chimney_od/2, chimney_h)
    chimney.translate(FreeCAD.Base.Vector(bridge_l/2 - 5, 0, BOX_HEIGHT_ABOVE_BOTTOM + bridge_h))

    chimney_hole = Part.makeCylinder(chimney_id/2, 11.0)
    chimney_hole.translate(FreeCAD.Base.Vector(bridge_l/2 - 5, 0, 48.0 - 11.0))
    chimney = chimney.cut(chimney_hole)

    hull = hull.fuse(chimney)

    # Add to document
    obj = doc.addObject("Part::Feature", "Benchy")
    obj.Shape = hull

    doc.recompute()

    save_fcstd(doc, "benchy.FCStd")
    export_stl([obj], "benchy.stl")

    print("Improved Benchy generated successfully.")

if __name__ == "__main__":
    create_benchy()
