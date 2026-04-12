import sys
import os
import math
from freecad_utils import setup_freecad

FreeCAD, Part, Mesh, PartDesign = setup_freecad()

def create_benchy():
    doc = FreeCAD.newDocument("Benchy")

    # --- Hull ---
    # Bottom profile (X from -20 to 15, Width 16)
    p1 = FreeCAD.Vector(-20, 0, 0)
    p2 = FreeCAD.Vector(0, 8, 0)
    p3 = FreeCAD.Vector(15, 0, 0)
    p4 = FreeCAD.Vector(0, -8, 0)
    wire1 = Part.makePolygon([p1, p2, p3, p4, p1])

    # Mid profile (wider, X from -25 to 25, Width 30)
    p5 = FreeCAD.Vector(-25, 0, 10)
    p6 = FreeCAD.Vector(0, 15, 10)
    p7 = FreeCAD.Vector(25, 0, 10)
    p8 = FreeCAD.Vector(0, -15, 10)
    wire2 = Part.makePolygon([p5, p6, p7, p8, p5])

    # Deck profile (at Z=15, X from -30 to 30, Width 31)
    p9 = FreeCAD.Vector(-30, 0, 15) # Stern
    p10 = FreeCAD.Vector(0, 15.5, 15)
    p11 = FreeCAD.Vector(30, 0, 15) # Bow
    p12 = FreeCAD.Vector(0, -15.5, 15)
    wire3 = Part.makePolygon([p9, p10, p11, p12, p9])

    hull_loft = Part.makeLoft([wire1, wire2, wire3], True)

    # --- Deck ---
    deck_shell = Part.makeFilledFace(wire3.Edges)
    deck = deck_shell.extrude(FreeCAD.Vector(0, 0, 1))
    deck.translate(FreeCAD.Vector(0,0,-0.5))

    # --- Cabin (Bridge) ---
    cabin_base = Part.makeBox(20, 20, 18)
    cabin_base.translate(FreeCAD.Vector(-15, -10, 15))

    # Windows
    front_window = Part.makeBox(0.5, 10.5, 9.5)
    front_window.translate(FreeCAD.Vector(4.5, -5.25, 20))

    rear_window_hole = Part.makeCylinder(4.5, 5) # Radius 4.5 = ID 9
    rear_window_hole.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,1,0), 90)
    rear_window_hole.translate(FreeCAD.Vector(-16, 0, 25))

    cabin_base = cabin_base.cut(front_window).cut(rear_window_hole)

    # Rear window flange
    rear_flange = Part.makeCylinder(6, 0.3) # Radius 6 = OD 12
    rear_flange.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,1,0), 90)
    rear_flange.translate(FreeCAD.Vector(-15.3, 0, 25))
    rear_flange = rear_flange.cut(rear_window_hole)

    # --- Roof ---
    roof = Part.makeBox(23, 22, 2)
    roof.translate(FreeCAD.Vector(-18, -11, 33))
    # Inclination 5.5 degrees
    roof.rotate(FreeCAD.Vector(-18, 0, 33), FreeCAD.Vector(0, 1, 0), -5.5)

    # --- Chimney ---
    chimney_outer = Part.makeCylinder(3.5, 15)
    chimney_inner = Part.makeCylinder(1.5, 16)
    chimney = chimney_outer.cut(chimney_inner)
    chimney.translate(FreeCAD.Vector(-5, 0, 33))

    # --- Cargo Box ---
    box_outer = Part.makeBox(12, 10.81, 9)
    box_inner = Part.makeBox(8, 7, 10)
    box_inner.translate(FreeCAD.Vector(2, 1.905, 1))
    cargo_box = box_outer.cut(box_inner)
    cargo_box.translate(FreeCAD.Vector(-28, -5.405, 15))

    # --- Hawsepipe ---
    hawse_outer = Part.makeCylinder(2, 5)
    hawse_outer.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,1,0), 90)
    hawse_outer.translate(FreeCAD.Vector(25, -5, 10))

    # Combine
    benchy = hull_loft.fuse(deck).fuse(cabin_base).fuse(roof).fuse(chimney).fuse(cargo_box).fuse(hawse_outer).fuse(rear_flange)

    # Stern Nameplate (0.1mm extrusion)
    nameplate = Part.makeBox(0.1, 10, 5)
    nameplate.translate(FreeCAD.Vector(-30.1, -5, 10))
    benchy = benchy.fuse(nameplate)

    # Export
    benchy_obj = doc.addObject("Part::Feature", "Benchy")
    benchy_obj.Shape = benchy

    doc.saveAs("benchy.fcstd")
    Mesh.export([benchy_obj], "benchy.stl")
    print("Exported benchy.fcstd and benchy.stl")

if __name__ == "__main__":
    create_benchy()
