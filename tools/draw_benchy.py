import os
import sys
import math

# Add the root directory to sys.path to find freecad_utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import freecad_utils

def create_benchy():
    FreeCAD = freecad_utils.init_freecad()
    import Part
    import Mesh

    doc = FreeCAD.newDocument("Benchy")

    # Dimensions
    L = 60.0
    W = 31.0
    H = 48.0

    # --- Hull Construction ---
    # Bottom Profile
    p1 = Part.makePolygon([
        FreeCAD.Vector(-18, 0, 0),
        FreeCAD.Vector(10, -7.5, 0),
        FreeCAD.Vector(18, 0, 0),
        FreeCAD.Vector(10, 7.5, 0),
        FreeCAD.Vector(-18, 0, 0)
    ])

    # Mid Profile (for better curvature)
    p2 = Part.makePolygon([
        FreeCAD.Vector(-24, 0, 7),
        FreeCAD.Vector(12, -12, 7),
        FreeCAD.Vector(24, 0, 7),
        FreeCAD.Vector(12, 12, 7),
        FreeCAD.Vector(-24, 0, 7)
    ])

    # Deck Profile
    p3 = Part.makePolygon([
        FreeCAD.Vector(-30, 0, 15),
        FreeCAD.Vector(15, -15.5, 15),
        FreeCAD.Vector(30, 0, 15),
        FreeCAD.Vector(15, 15.5, 15),
        FreeCAD.Vector(-30, 0, 15)
    ])

    # Convert polygons to wires and then to loft
    w1 = Part.Wire(p1.Edges)
    w2 = Part.Wire(p2.Edges)
    w3 = Part.Wire(p3.Edges)
    hull = Part.makeLoft([w1, w2, w3], True)

    # --- Deck ---
    deck = Part.makeBox(20, 31, 2)
    deck.translate(FreeCAD.Vector(-15, -15.5, 13))

    # --- Cabin ---
    cabin_base = Part.makeBox(23, 23, 21)
    cabin_base.translate(FreeCAD.Vector(-15, -11.5, 15))

    # Cabin door/windows
    door = Part.makeBox(10, 1, 15)
    door.translate(FreeCAD.Vector(-5, 11.5, 15))
    window1 = Part.makeBox(8, 1, 8)
    window1.translate(FreeCAD.Vector(-10, -11.5, 22))

    cabin = cabin_base.cut(door).cut(window1)

    # --- Roof ---
    roof = Part.makeBox(26, 26, 2)
    roof.translate(FreeCAD.Vector(-16, -13, 36))
    # Slight inclination (5.5 degrees)
    roof.rotate(FreeCAD.Vector(-16, 0, 36), FreeCAD.Vector(0, 1, 0), -5.5)

    # --- Chimney ---
    chimney_outer = Part.makeCylinder(3.5, 11)
    chimney_inner = Part.makeCylinder(1.5, 12)
    chimney = chimney_outer.cut(chimney_inner)
    chimney.translate(FreeCAD.Vector(0, 0, 37))

    # --- Cargo Box ---
    cargo = Part.makeBox(12, 12, 9)
    cargo.translate(FreeCAD.Vector(-28, -6, 15))

    # Combine everything
    benchy_shape = hull.fuse(deck).fuse(cabin).fuse(roof).fuse(chimney).fuse(cargo)

    # Center the model and ensure dimensions
    bbox = benchy_shape.BoundBox
    center_offset = FreeCAD.Vector(
        -(bbox.XMin + bbox.XMax)/2,
        -(bbox.YMin + bbox.YMax)/2,
        -bbox.ZMin
    )
    benchy_shape.translate(center_offset)

    final_bbox = benchy_shape.BoundBox
    print(f"Final Bounding Box: {final_bbox.XLength:.2f} x {final_bbox.YLength:.2f} x {final_bbox.ZLength:.2f}")

    # Save FCStd
    obj = doc.addObject("Part::Feature", "Benchy")
    obj.Shape = benchy_shape
    doc.recompute()

    if not os.path.exists("output"):
        os.makedirs("output")

    output_fcstd = "output/benchy.FCStd"
    doc.saveAs(output_fcstd)
    print(f"Saved {output_fcstd}")

    # Export STL
    output_stl = "output/benchy.stl"
    Mesh.export([obj], output_stl)
    print(f"Exported {output_stl}")

if __name__ == "__main__":
    create_benchy()
