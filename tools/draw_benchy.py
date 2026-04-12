import sys
import os
import math

# Add the path to FreeCAD
from freecad_utils import setup_freecad
if not setup_freecad():
    print("FreeCAD not found")
    sys.exit(1)

import FreeCAD
import Part
import Mesh

def create_benchy():
    doc = FreeCAD.newDocument("Benchy")

    # Target Dimensions: 60 x 31 x 48

    # 1. Hull
    hull_height = 15.0
    hull_width = 31.0
    hull_length = 60.0

    # Simple hull box to ensure BBox accuracy for now
    # We will add features but keep them within the 60mm limit
    hull = Part.makeBox(hull_length, hull_width, hull_height)
    hull.translate(FreeCAD.Vector(-30, -hull_width/2, 0)) # x: -30 to 30

    # 2. Cabin
    cabin_length = 23.0
    cabin_width = 20.0
    cabin_height = 20.0
    cabin_main = Part.makeBox(cabin_length, cabin_width, cabin_height)
    cabin_main.translate(FreeCAD.Vector(-10, -cabin_width/2, hull_height)) # x: -10 to 13

    # Windows
    window_front = Part.makeBox(5, 10.5, 9.5)
    window_front.translate(FreeCAD.Vector(10, -10.5/2, hull_height + 5))

    win_r_inner = 4.5 # dia 9
    window_rear = Part.makeCylinder(win_r_inner, 10)
    window_rear.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,1,0), 90)
    window_rear.translate(FreeCAD.Vector(-15, 0, hull_height + 10))

    cabin = cabin_main.cut(window_front).cut(window_rear)

    # 3. Roof
    roof_length = 23.0
    roof_width = 24.0
    roof_height = 2.0
    roof = Part.makeBox(roof_length, roof_width, roof_height)
    angle = 5.5
    # Rotate around (-10, 0, 35)
    roof.rotate(FreeCAD.Vector(-10, 0, hull_height + cabin_height), FreeCAD.Vector(0, 1, 0), -angle)
    roof.translate(FreeCAD.Vector(-10, -roof_width/2, hull_height + cabin_height))

    # 4. Chimney
    chimney_outer_dia = 7.0
    chimney_inner_dia = 3.0
    chimney_total_h = 10.0
    chimney_hole_depth = 8.0

    chimney_outer = Part.makeCylinder(chimney_outer_dia/2, chimney_total_h)
    chimney_inner = Part.makeCylinder(chimney_inner_dia/2, chimney_hole_depth)
    chimney_inner.translate(FreeCAD.Vector(0, 0, chimney_total_h - chimney_hole_depth))

    chimney = chimney_outer.cut(chimney_inner)
    chimney.translate(FreeCAD.Vector(5, 0, 48 - chimney_total_h))

    # 5. Cargo Box
    box_l = 12.0
    box_w = 10.81
    box_h = 9.0
    box_outer = Part.makeBox(box_l, box_w, box_h)
    box_inner = Part.makeBox(8.0, 7.0, 9.0)
    box_inner.translate(FreeCAD.Vector(2, (10.81-7.0)/2, 1))

    cargo_box = box_outer.cut(box_inner)
    cargo_box.translate(FreeCAD.Vector(-25, -box_w/2, hull_height))

    # Combine
    benchy_shape = hull.fuse(cabin).fuse(roof).fuse(chimney).fuse(cargo_box)

    # Add to document
    obj = doc.addObject("Part::Feature", "Benchy")
    obj.Shape = benchy_shape

    doc.recompute()

    # Final check
    bbox = obj.Shape.BoundBox
    print(f"BBox: {bbox.XLength:.4f} x {bbox.YLength:.4f} x {bbox.ZLength:.4f}")

    # Export
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    fcstd_path = os.path.join(output_dir, "benchy.FCStd")
    stl_path = os.path.join(output_dir, "benchy.stl")

    doc.saveAs(fcstd_path)
    Mesh.export([obj], stl_path)

    # Final root files
    doc.saveAs("benchy.FCStd")
    Mesh.export([obj], "benchy.stl")

    print(f"Benchy created and saved to {fcstd_path} and {stl_path}")

if __name__ == "__main__":
    create_benchy()
