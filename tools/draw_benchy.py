import sys
import os
import math

# Use the discovery utility to set up the FreeCAD environment.
try:
    from freecad_utils import setup_freecad
    if not setup_freecad():
        print("FreeCAD environment setup failed.")
        sys.exit(1)
except ImportError:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(script_dir)
    from freecad_utils import setup_freecad
    if not setup_freecad():
         print("FreeCAD environment setup failed.")
         sys.exit(1)

import FreeCAD
import Part

def create_benchy():
    # Create a new document
    doc = FreeCAD.newDocument("Benchy")

    # Dimensions from specs
    length = 60.0
    width = 31.0
    height = 48.0

    # 1. Hull (Bottom half)
    # Main hull body
    hull_l = 45.0
    hull_box = Part.makeBox(hull_l, width, 10)
    hull_box.Placement = FreeCAD.Placement(FreeCAD.Vector(-30, -width/2, 0), FreeCAD.Rotation())

    # Bow (Wedge-like with overhang)
    # A 40 degree overhang from vertical means 50 degrees from horizontal.
    # Using a wedge to approximate the bow.
    bow_l = 15.0
    bow_h = 15.0
    # makeWedge(xmin, ymin, zmin, z2min, x2min, xmax, ymax, zmax, z2max, x2max, ltx)
    # The 12-argument version: makeWedge(xmin, ymin, zmin, x2min, y2min, z2min, xmax, ymax, zmax, x2max, y2max, z2max)
    # Let's use a simpler approach: make a box and cut it with a tilted plane.
    bow_box = Part.makeBox(bow_l, width, bow_h)
    bow_box.Placement = FreeCAD.Placement(FreeCAD.Vector(15, -width/2, 0), FreeCAD.Rotation())

    # Tilted cutting box for bow overhang (40 deg from vertical)
    cutter = Part.makeBox(bow_l * 2, width * 2, bow_h * 2)
    # Rotate cutter by 40 degrees around Y axis
    cutter_rot = FreeCAD.Rotation(FreeCAD.Vector(0, 1, 0), 40)
    cutter.Placement = FreeCAD.Placement(FreeCAD.Vector(15, -width, 0), cutter_rot)

    bow = bow_box.cut(cutter)

    hull = hull_box.fuse(bow)

    # 2. Deck
    deck = Part.makeBox(length, width, 2)
    deck.Placement = FreeCAD.Placement(FreeCAD.Vector(-30, -width/2, 10), FreeCAD.Rotation())

    # 3. Cabin (Bridge)
    cabin_w = 20.0
    cabin_l = 25.0
    cabin_h = 20.0
    cabin = Part.makeBox(cabin_l, cabin_w, cabin_h)
    cabin.Placement = FreeCAD.Placement(FreeCAD.Vector(-10, -cabin_w/2, 12), FreeCAD.Rotation())

    # Hollow out cabin
    inner_cabin = Part.makeBox(cabin_l-4, cabin_w-4, cabin_h)
    inner_cabin.Placement = FreeCAD.Placement(FreeCAD.Vector(-8, -(cabin_w-4)/2, 12), FreeCAD.Rotation())
    cabin = cabin.cut(inner_cabin)

    # 4. Roof
    roof_w = cabin_w + 4.0
    roof_l = cabin_l + 4.0
    roof_h = 2.0
    roof = Part.makeBox(roof_l, roof_w, roof_h)
    # Tilt roof slightly (5.5 deg)
    roof_tilt = FreeCAD.Rotation(FreeCAD.Vector(0, 1, 0), 5.5)
    roof.Placement = FreeCAD.Placement(FreeCAD.Vector(-12, -roof_w/2, 12 + cabin_h), roof_tilt)

    # 5. Chimney
    chimney_od = 7.0
    chimney_id = 3.0
    chimney_h = 11.0
    chimney_outer = Part.makeCylinder(chimney_od/2, chimney_h)
    chimney_inner = Part.makeCylinder(chimney_id/2, chimney_h)
    chimney = chimney_outer.cut(chimney_inner)
    chimney.Placement = FreeCAD.Placement(FreeCAD.Vector(5, 0, 12 + cabin_h + 1), FreeCAD.Rotation())

    # Fuse all parts
    benchy = hull.fuse(deck).fuse(cabin).fuse(roof).fuse(chimney)

    # Add to document
    benchy_obj = doc.addObject("Part::Feature", "BenchyModel")
    benchy_obj.Shape = benchy

    # Ensure output directory exists
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save the document
    doc.saveAs(os.path.join(output_dir, "benchy.fcstd"))

    # Export to STL
    Part.export([benchy_obj], os.path.join(output_dir, "benchy.stl"))

    print(f"Benchy model created successfully in {output_dir}/")

if __name__ == "__main__":
    create_benchy()
