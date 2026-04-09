import sys
import os
import math

# Setup FreeCAD path
from freecad_utils import setup_freecad
if not setup_freecad():
    print("FreeCAD library not found!")
    sys.exit(1)

import FreeCAD
import Part
import Mesh

def create_hull(doc):
    # Dimensions
    length = 60.0
    width = 31.0
    height_to_deck = 15.5
    bow_angle = 40.0 # to horizontal

    overhang = height_to_deck / math.tan(math.radians(bow_angle))
    hull_body_l = length - overhang

    # Main hull body (box)
    hull_body = Part.makeBox(hull_body_l, width, height_to_deck, FreeCAD.Vector(0, -width/2, 0))

    # Bow (wedge)
    bow = Part.makeWedge(0, -width/2, 0, 0, -width/2, overhang, width/2, height_to_deck, overhang, width/2)
    bow.translate(FreeCAD.Vector(hull_body_l, 0, 0))

    hull = hull_body.fuse(bow)

    # Hawsepipes
    hp_radius = 2.0 # 4.0 diameter
    hp_y = 12.0
    hp_z = 12.0
    hp_x = length - 5.0
    hp_left = Part.makeCylinder(hp_radius, 10, FreeCAD.Vector(hp_x, -hp_y, hp_z), FreeCAD.Vector(-1, 0, 0))
    hp_right = Part.makeCylinder(hp_radius, 10, FreeCAD.Vector(hp_x, hp_y, hp_z), FreeCAD.Vector(-1, 0, 0))

    hull = hull.cut(hp_left).cut(hp_right)

    hull_obj = doc.addObject("Part::Feature", "Hull")
    hull_obj.Shape = hull
    return hull_obj

def create_deck(doc):
    # Dimensions
    box_outer_l = 12.0
    box_outer_w = 10.81
    box_inner_l = 8.0
    box_inner_w = 7.0
    box_depth = 9.0
    height_to_deck = 15.5

    # Cargo box
    outer_box = Part.makeBox(box_outer_l, box_outer_w, box_depth, FreeCAD.Vector(5, -box_outer_w/2, height_to_deck))
    inner_box = Part.makeBox(box_inner_l, box_inner_w, box_depth, FreeCAD.Vector(5 + (box_outer_l-box_inner_l)/2, -box_inner_w/2, height_to_deck + 1))

    cargo_box = outer_box.cut(inner_box)

    box_obj = doc.addObject("Part::Feature", "CargoBox")
    box_obj.Shape = cargo_box
    return box_obj

def create_cabin(doc):
    # Dimensions
    height_to_deck = 15.5
    cabin_l = 23.0
    cabin_w = 20.0
    cabin_h = 20.0
    roof_angle = 5.5

    # Cabin base
    cabin_base = Part.makeBox(cabin_l, cabin_w, cabin_h, FreeCAD.Vector(25, -cabin_w/2, height_to_deck))

    # Roof cut (inclined plane)
    # Plane equation: z = h_max - tan(angle) * (x - x_min)
    # We want it to slope down towards stern (-X).
    # But in our setup stern is at 0, bow at +60.
    # So roof should slope down towards stern: z decreases as X decreases.
    # Highest point at bow side of cabin (X=25+23=48).

    roof_extra_h = cabin_l * math.tan(math.radians(roof_angle))
    cutter = Part.makeBox(cabin_l + 2, cabin_w + 2, cabin_h, FreeCAD.Vector(24, -cabin_w/2 - 1, height_to_deck + cabin_h))
    # Rotate cutter around Y axis at the front of the cabin
    cutter.rotate(FreeCAD.Vector(48, 0, height_to_deck + cabin_h), FreeCAD.Vector(0, 1, 0), -roof_angle)

    cabin = cabin_base.cut(cutter)

    # Front Window
    window_w = 10.5
    window_h = 9.5
    window_front = Part.makeBox(5, window_w, window_h, FreeCAD.Vector(48-2, -window_w/2, height_to_deck + 5))

    # Rear Window (Circular)
    rw_radius = 4.5 # 9.0 diameter
    window_rear = Part.makeCylinder(rw_radius, 5, FreeCAD.Vector(25, 0, height_to_deck + 10), FreeCAD.Vector(1, 0, 0))

    cabin = cabin.cut(window_front).cut(window_rear)

    cabin_obj = doc.addObject("Part::Feature", "Cabin")
    cabin_obj.Shape = cabin
    return cabin_obj

def create_chimney(doc):
    # Dimensions
    od = 7.0
    id = 3.0
    total_height = 48.0
    depth = 11.0
    height_to_deck = 15.5
    cabin_h = 20.0
    chimney_base_z = height_to_deck + cabin_h - 2 # embedded slightly
    h = total_height - chimney_base_z

    outer = Part.makeCylinder(od/2, h, FreeCAD.Vector(35, 0, chimney_base_z))
    inner = Part.makeCylinder(id/2, depth, FreeCAD.Vector(35, 0, chimney_base_z + h - depth))

    chimney = outer.cut(inner)

    chimney_obj = doc.addObject("Part::Feature", "Chimney")
    chimney_obj.Shape = chimney
    return chimney_obj

def create_benchy():
    doc = FreeCAD.newDocument("Benchy")

    hull = create_hull(doc)
    deck = create_deck(doc)
    cabin = create_cabin(doc)
    chimney = create_chimney(doc)

    doc.recompute()
    return doc

if __name__ == "__main__":
    doc = create_benchy()
    # Save the document
    output_path = "benchy.FCStd"
    doc.saveAs(output_path)
    print(f"Document saved to {output_path}")

    # Export STL
    objs = doc.Objects
    Mesh.export(objs, "benchy.stl")
    print("STL exported to benchy.stl")

    # Export SCAD
    try:
        openscad_mod_path = "/usr/share/freecad/Mod/OpenSCAD/"
        if os.path.exists(openscad_mod_path) and openscad_mod_path not in sys.path:
            sys.path.append(openscad_mod_path)
        import exportCSG
        if not hasattr(exportCSG, 'pythonopen'):
            exportCSG.pythonopen = open
        exportCSG.export(objs, "benchy.scad")
        print("SCAD exported to benchy.scad")
    except Exception as e:
        print(f"Failed to export SCAD: {e}")
