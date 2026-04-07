import sys
import os
import math

# Import our utility to setup FreeCAD path
from freecad_utils import setup_freecad
if not setup_freecad():
    # Attempt to locate FreeCAD manually if utility fails
    potential_paths = [
        "/usr/lib/freecad-python3/lib",
        "/usr/lib/freecad/lib",
    ]
    for path in potential_paths:
        if os.path.exists(path):
            sys.path.append(path)
            break

import FreeCAD as App
import Part
import Mesh

def create_benchy():
    doc = App.newDocument("Benchy")

    # --- Hull Parameters ---
    total_length = 60.0
    total_width = 31.0
    total_height = 48.0

    # --- 1. Hull Base ---
    p1 = App.Vector(-30, 0, 0)
    p2 = App.Vector(0, -15.5, 0)
    p3 = App.Vector(30, -15.5, 0)
    p4 = App.Vector(30, 15.5, 0)
    p5 = App.Vector(0, 15.5, 0)

    edge1 = Part.makePolygon([p1, p2, p3, p4, p5, p1])
    hull_face = Part.Face(edge1)
    hull_bottom = hull_face.extrude(App.Vector(0, 0, 15.5))

    # --- 2. Deck & Cargo Box ---
    cargo_box_outer = Part.makeBox(12.0, 10.81, 9.0)
    cargo_box_outer.translate(App.Vector(15, -5.405, 15.5))

    cargo_box_inner = Part.makeBox(8.0, 7.0, 9.0)
    cargo_box_inner.translate(App.Vector(17, -3.5, 15.5 + 0.1)) # Small offset to avoid z-fighting
    cargo_box = cargo_box_outer.cut(cargo_box_inner)

    # --- 3. Bridge (Cabin) ---
    bridge = Part.makeBox(23.0, 25.0, 20.0)
    bridge.translate(App.Vector(-15, -12.5, 15.5))

    # --- 4. Chimney ---
    chimney_outer = Part.makeCylinder(3.5, 15.0)
    chimney_outer.translate(App.Vector(-5, 0, 33.0))

    chimney_inner = Part.makeCylinder(1.5, 11.0)
    chimney_inner.translate(App.Vector(-5, 0, 37.0))

    chimney = chimney_outer.cut(chimney_inner)

    # --- Combine All ---
    benchy_shape = hull_bottom.fuse(cargo_box).fuse(bridge).fuse(chimney)

    # Final Precise Scaling to ensure 60x31x48 exactly
    bbox = benchy_shape.BoundBox
    curr_l = bbox.XMax - bbox.XMin
    curr_w = bbox.YMax - bbox.YMin
    curr_h = bbox.ZMax - bbox.ZMin

    scale_x = total_length / curr_l if curr_l > 0 else 1.0
    scale_y = total_width / curr_w if curr_w > 0 else 1.0
    scale_z = total_height / curr_h if curr_h > 0 else 1.0

    mat = App.Matrix()
    mat.scale(scale_x, scale_y, scale_z)
    benchy_shape.transformShape(mat)

    # Reset position so it's centered and starts at z=0
    bbox = benchy_shape.BoundBox
    benchy_shape.translate(App.Vector(-bbox.XMin - (total_length/2), -bbox.YMin - (total_width/2), -bbox.ZMin))

    benchy_obj = doc.addObject("Part::Feature", "Benchy")
    benchy_obj.Shape = benchy_shape

    doc.recompute()

    # Export
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    fcstd_path = os.path.join(output_dir, "benchy.FCStd")
    stl_path = os.path.join(output_dir, "benchy.stl")

    doc.saveAs(fcstd_path)

    # Export STL
    # Use Mesh.write/read as per memory for headless
    mesh_obj = doc.addObject("Mesh::Feature", "BenchyMesh")
    import MeshPart
    mesh_obj.Mesh = MeshPart.meshFromShape(Shape=benchy_obj.Shape, MaxLength=0.5)
    mesh_obj.Mesh.write(stl_path)

    print(f"Benchy generated at {fcstd_path} and {stl_path}")
    print(f"Final Bounding Box: {benchy_obj.Shape.BoundBox}")

if __name__ == "__main__":
    create_benchy()
