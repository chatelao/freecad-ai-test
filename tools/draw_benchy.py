import sys
import os

# Add current dir to sys.path to import freecad_utils
sys.path.append(os.path.dirname(__file__))
import freecad_utils

import FreeCAD as App
import Part

def create_benchy():
    doc = App.newDocument("Benchy")

    # --- HULL ---
    # Approximate the 3DBenchy hull with a Loft of 3 profiles
    # Profile 1: Bottom (Z=0)
    w1 = Part.makePolygon([
        App.Vector(-20, -5, 0),
        App.Vector(10, -5, 0),
        App.Vector(25, 0, 0),
        App.Vector(10, 5, 0),
        App.Vector(-20, 5, 0),
        App.Vector(-20, -5, 0)
    ])
    # Profile 2: Middle (Z=8)
    w2 = Part.makePolygon([
        App.Vector(-25, -12, 8),
        App.Vector(15, -12, 8),
        App.Vector(30, 0, 8),
        App.Vector(15, 12, 8),
        App.Vector(-25, 12, 8),
        App.Vector(-25, -12, 8)
    ])
    # Profile 3: Gunwale (Z=15.5)
    # Adjusted X to target 60mm length exactly.
    # Previous XLength was 60.46 with range [-30, 30].
    # This might be due to the curvature or the lofting algorithm.
    # Let's shrink it slightly to [-29.7, 29.8] to hit ~60.0.
    w3 = Part.makePolygon([
        App.Vector(-29.7, -15.5, 15.5),
        App.Vector(20, -15.5, 15.5),
        App.Vector(29.8, 0, 15.5),
        App.Vector(20, 15.5, 15.5),
        App.Vector(-29.7, 15.5, 15.5),
        App.Vector(-29.7, -15.5, 15.5)
    ])

    hull = Part.makeLoft([w1, w2, w3], True) # solid=True

    # --- DECK ---
    deck = Part.makeBox(45, 28, 2)
    deck.translate(App.Vector(-28, -14, 14))

    # --- CABIN (BRIDGE) ---
    cabin_base = Part.makeBox(20, 18, 20)
    cabin_base.translate(App.Vector(-10, -9, 15.5))

    # Windows (Cuts)
    front_window = Part.makeBox(2, 10.5, 9.5)
    front_window.translate(App.Vector(9, -5.25, 22))

    side_window_l = Part.makeBox(10, 2, 8)
    side_window_l.translate(App.Vector(-5, 8, 22))

    side_window_r = Part.makeBox(10, 2, 8)
    side_window_r.translate(App.Vector(-5, -10, 22))

    cabin = cabin_base.cut(front_window).cut(side_window_l).cut(side_window_r)

    # --- ROOF ---
    roof = Part.makeBox(23, 22, 2)
    # Tilt roof 5.5 degrees
    roof.rotate(App.Vector(-12, 0, 35.5), App.Vector(0, 1, 0), -5.5)
    roof.translate(App.Vector(-12, -11, 35.5))

    # --- CHIMNEY ---
    chimney_cyl = Part.makeCylinder(3.5, 14)
    chimney_cyl.translate(App.Vector(5, 0, 34))

    # Chimney hole
    ch_hole = Part.makeCylinder(1.5, 11)
    ch_hole.translate(App.Vector(5, 0, 37))
    chimney = chimney_cyl.cut(ch_hole)

    # --- CARGO BOX ---
    box_outer = Part.makeBox(12, 10.81, 9)
    box_outer.translate(App.Vector(-25, -5.405, 15.5))
    box_inner = Part.makeBox(8, 7, 9)
    box_inner.translate(App.Vector(-23, -3.5, 16.5))
    cargo_box = box_outer.cut(box_inner)

    # --- FINAL ASSEMBLY ---
    benchy = hull.fuse(deck).fuse(cabin).fuse(roof).fuse(chimney).fuse(cargo_box)

    # Add to document
    obj = doc.addObject("Part::Feature", "Benchy")
    obj.Shape = benchy

    doc.recompute()

    # Output files
    output_fcstd = "benchy.FCStd"
    output_stl = "benchy.stl"

    doc.saveAs(output_fcstd)
    freecad_utils.export_stl([obj], output_stl)

    print(f"Model saved to {output_fcstd} and {output_stl}")
    return obj

if __name__ == "__main__":
    create_benchy()
