import os
import sys
from freecad_utils import setup_freecad

if not setup_freecad():
    print("Error: FreeCAD could not be loaded.")
    sys.exit(1)

import FreeCAD
import Part
import Mesh
import math

def create_benchy():
    doc = FreeCAD.newDocument("Benchy")

    # Dimensions (mm)
    L = 60.0
    W = 31.0
    H = 48.0
    DECK_H = 15.5
    BOW_ANGLE = 40.0 # deg to horizontal
    ROOF_ANGLE = 5.5 # deg

    # --- 1. Simple Hull (to avoid loft errors) ---
    bow_bottom_x = L - (DECK_H / math.tan(math.radians(BOW_ANGLE)))

    # Create the bottom profile (3 points)
    p1 = FreeCAD.Vector(0, -W*0.3, 0)
    p2 = FreeCAD.Vector(0, W*0.3, 0)
    p3 = FreeCAD.Vector(bow_bottom_x, 0, 0)
    bottom_wire = Part.makePolygon([p1, p2, p3, p1])

    # Create the deck profile (3 points)
    dp1 = FreeCAD.Vector(0, -W/2, DECK_H)
    dp2 = FreeCAD.Vector(0, W/2, DECK_H)
    dp3 = FreeCAD.Vector(L, 0, DECK_H)
    deck_wire = Part.makePolygon([dp1, dp2, dp3, dp1])

    # Loft the hull
    hull_shell = Part.makeLoft([bottom_wire, deck_wire], True)
    hull = Part.Solid(hull_shell)

    # --- 2. Deck and Cargo Box ---
    # Cargo box: 12.0 x 10.81 outside, 8.0 x 7.0 inside, 9.0 deep.
    box_outer = Part.makeBox(12.0, 10.81, 9.0)
    box_outer.translate(FreeCAD.Vector(5, -10.81/2, DECK_H))

    box_inner = Part.makeBox(8.0, 7.0, 10.0) # slightly taller to ensure clean cut
    box_inner.translate(FreeCAD.Vector(7, -3.5, DECK_H + 1.0)) # 1mm bottom

    cargo_box = box_outer.cut(box_inner)

    # --- 3. Cabin (Bridge) ---
    cabin_l = 23.0
    cabin_w = 22.0
    cabin_h = 20.0
    cabin_x = 22.0

    cabin_base = Part.makeBox(cabin_l, cabin_w, cabin_h)
    cabin_base.translate(FreeCAD.Vector(cabin_x, -cabin_w/2, DECK_H))

    # Roof inclination 5.5 deg
    roof_cut = Part.makeBox(cabin_l * 2, cabin_w * 2, 10)
    roof_cut.translate(FreeCAD.Vector(-cabin_l/2, -cabin_w, cabin_h))
    roof_cut.rotate(FreeCAD.Vector(cabin_x + cabin_l, 0, DECK_H + cabin_h), FreeCAD.Vector(0, 1, 0), ROOF_ANGLE)

    cabin = cabin_base.cut(roof_cut)

    # Windows
    # Front Window: 10.5 x 9.5
    win_f = Part.makeBox(5, 10.5, 9.5)
    win_f.translate(FreeCAD.Vector(cabin_x + cabin_l - 2, -10.5/2, DECK_H + 5))
    cabin = cabin.cut(win_f)

    # Rear Window: Inner 9.0 mm (Circular)
    win_r_cyl = Part.makeCylinder(9.0/2, 5.0)
    win_r_cyl.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,1,0), 90)
    win_r_cyl.translate(FreeCAD.Vector(cabin_x - 2, 0, DECK_H + 10))
    cabin = cabin.cut(win_r_cyl)

    # --- 4. Chimney ---
    # OD 7, ID 3, Depth 11.
    chim_h = 15.0
    chim_od = 7.0
    chim_id = 3.0
    chimney_outer = Part.makeCylinder(chim_od/2, chim_h)
    chimney_inner = Part.makeCylinder(chim_id/2, 11.0)
    chimney_inner.translate(FreeCAD.Vector(0, 0, chim_h - 11.0))
    chimney = chimney_outer.cut(chimney_inner)

    # Position chimney on cabin roof, adjust to hit 48mm total height
    chimney.translate(FreeCAD.Vector(cabin_x + 5, 0, DECK_H + cabin_h - 2.5))

    # --- 5. Hawsepipe ---
    # Inner diameter 4.0 mm
    hawse = Part.makeCylinder(4.0/2, 10.0)
    hawse.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,1,0), 90)
    hawse.translate(FreeCAD.Vector(L - 10, -W/4, DECK_H - 5))

    # --- 6. Nameplate ---
    # 0.1mm extrusion at stern
    nameplate = Part.makeBox(0.1, 10, 5)
    nameplate.translate(FreeCAD.Vector(-0.1, -5, DECK_H - 10))

    # Merge all
    benchy = hull.fuse(cargo_box).fuse(cabin).fuse(chimney).fuse(nameplate).cut(hawse)

    # Final Model
    doc.addObject("Part::Feature", "Benchy").Shape = benchy
    doc.recompute()

    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    doc.saveAs(os.path.join(output_dir, "benchy.FCStd"))
    Mesh.export([doc.Benchy], os.path.join(output_dir, "benchy.stl"))

    print("Improved Benchy created successfully in output/ directory.")

if __name__ == "__main__":
    create_benchy()
