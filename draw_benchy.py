import os
import sys
import argparse
import shutil

# Add tools directory to path to import freecad_utils
sys.path.append(os.path.join(os.path.dirname(__file__), 'tools'))
import freecad_utils

if not freecad_utils.setup_freecad_path():
    print("Error: Could not find FreeCAD library.")
    sys.exit(1)

import FreeCAD
import Part
import Mesh
import math

def create_benchy():
    doc = FreeCAD.newDocument("Benchy")

    # 1. Hull
    # Side points for hull
    p1 = FreeCAD.Vector(-30, -10, 0)
    p2 = FreeCAD.Vector(-30, 10, 0)
    p3 = FreeCAD.Vector(10, 15.5, 0)
    p4 = FreeCAD.Vector(30, 0, 0)
    p5 = FreeCAD.Vector(10, -15.5, 0)

    hull_profile = Part.makePolygon([p1, p2, p3, p4, p5, p1])
    hull_face = Part.Face(hull_profile)
    hull_solid = hull_face.extrude(FreeCAD.Vector(0, 0, 15.5))

    # 1.1 Bow Overhang (40°)
    # 40 deg to horizontal.
    # deltaX = height / tan(40)
    dx = 15.5 / math.tan(math.radians(40))
    cut_pts = [
        FreeCAD.Vector(30, -20, 15.5),
        FreeCAD.Vector(30 - dx, -20, 0),
        FreeCAD.Vector(40, -20, 0),
        FreeCAD.Vector(40, -20, 15.5),
        FreeCAD.Vector(30, -20, 15.5)
    ]
    bow_cut_face = Part.Face(Part.makePolygon(cut_pts))
    bow_cut_solid = bow_cut_face.extrude(FreeCAD.Vector(0, 40, 0))
    hull_solid = hull_solid.cut(bow_cut_solid)

    # 2. Cabin
    # Height: The spec says "overall height 48mm".
    # If the chimney is at the top, it should be 48mm.
    # Let's make the bridge roof at 38mm and the chimney 10mm tall.
    c1 = FreeCAD.Vector(-15, -10, 15.5)
    c2 = FreeCAD.Vector(8, -10, 15.5)
    c3 = FreeCAD.Vector(8, 10, 15.5)
    c4 = FreeCAD.Vector(-15, 10, 15.5)

    cabin_profile = Part.makePolygon([c1, c2, c3, c4, c1])
    cabin_face = Part.Face(cabin_profile)
    cabin_solid = cabin_face.extrude(FreeCAD.Vector(0, 0, 38 - 15.5)) # Bridge roof at 38

    # 3. Roof Inclination (5.5°)
    angle = 5.5
    rad = math.radians(angle)
    z_diff = 23 * math.tan(rad)
    z_back = 38.0 - z_diff

    r1 = FreeCAD.Vector(8, -15, 38)
    r2 = FreeCAD.Vector(10, -15, 40)
    r3 = FreeCAD.Vector(-20, -15, 40)
    r4 = FreeCAD.Vector(-20, -15, z_back)

    roof_cut_profile = Part.makePolygon([r1, r2, r3, r4, r1])
    roof_cut_face = Part.Face(roof_cut_profile)
    roof_cut_solid = roof_cut_face.extrude(FreeCAD.Vector(0, 30, 0))
    cabin_solid = cabin_solid.cut(roof_cut_solid)

    # 4. Chimney
    # Overall height 48mm. Bridge roof 38mm. Chimney 10mm.
    chimney_base = FreeCAD.Vector(0, 0, 38)
    chimney_cyl = Part.makeCylinder(3.5, 10.0, chimney_base, FreeCAD.Vector(0, 0, 1))
    # Blind hole 11mm deep. From top (48).
    chimney_hole_base = FreeCAD.Vector(0, 0, 48 - 11)
    chimney_hole = Part.makeCylinder(1.5, 11.5, chimney_hole_base, FreeCAD.Vector(0, 0, 1))
    chimney_solid = chimney_cyl.cut(chimney_hole)

    # 5. Cargo Box (recessed)
    box_inside = Part.makeBox(8, 7, 9)
    box_inside.translate(FreeCAD.Vector(-23, -3.5, 15.5 - 9))
    hull_solid = hull_solid.cut(box_inside)

    # 6. Hawsepipe
    hp_cyl = Part.makeCylinder(2.0, 5.0, FreeCAD.Vector(25, -12, 10), FreeCAD.Vector(0, 1, 0))
    hull_solid = hull_solid.cut(hp_cyl)
    hp_cyl2 = Part.makeCylinder(2.0, 5.0, FreeCAD.Vector(25, 7, 10), FreeCAD.Vector(0, 1, 0))
    hull_solid = hull_solid.cut(hp_cyl2)

    # 7. Stern Nameplate
    nameplate = Part.makeBox(0.1, 15.0, 5.0)
    nameplate.translate(FreeCAD.Vector(-30, -7.5, 5.0))

    # Combine everything
    benchy = hull_solid.fuse(cabin_solid).fuse(chimney_solid).fuse(nameplate)

    obj = doc.addObject("Part::Feature", "Benchy")
    obj.Shape = benchy

    doc.recompute()
    return doc

def export_files(doc):
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    fcstd_path = os.path.join(output_dir, "benchy.FCStd")
    doc.saveAs(fcstd_path)

    stl_path = os.path.join(output_dir, "benchy.stl")
    obj = doc.getObject("Benchy")
    import MeshPart
    mesh = MeshPart.meshFromShape(obj.Shape, 0.1)
    mesh.write(stl_path)

    shutil.copy(fcstd_path, "benchy.FCStd")
    shutil.copy(stl_path, "benchy.stl")

    return fcstd_path, stl_path

if __name__ == "__main__":
    doc = create_benchy()
    export_files(doc)
