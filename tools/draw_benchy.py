import sys
import os
import math

from freecad_utils import setup_freecad

FreeCAD, Part, PartDesign, Mesh, TechDraw = setup_freecad()

def draw_benchy():
    doc = FreeCAD.newDocument("Benchy")

    # Dimensions
    L = 60.0
    W = 31.0
    H_hull = 15.0
    H_total = 48.0

    # 1. Hull
    hull_box = Part.makeBox(40, W, H_hull)

    # Bow part (wedge)
    bow_wedge = Part.makeWedge(0, 0, 0, 0, 0, 20, W, H_hull, 0, W/2)
    bow_wedge.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1), 180)
    bow_wedge.translate(FreeCAD.Vector(60, W, 0))

    hull_obj = doc.addObject("Part::Feature", "Hull")
    hull_obj.Shape = hull_box.fuse(bow_wedge)

    # 2. Cabin
    cabin_l = 25.0
    cabin_w = 20.0
    cabin_h = 20.0
    cabin = Part.makeBox(cabin_l, cabin_w, cabin_h)
    cabin.translate(FreeCAD.Vector(10, (W - cabin_w) / 2, H_hull))

    window1 = Part.makeBox(10, 5, 8)
    window1.translate(FreeCAD.Vector(15, (W - cabin_w) / 2 - 2.5, H_hull + 7))
    window2 = Part.makeBox(10, 5, 8)
    window2.translate(FreeCAD.Vector(15, (W + cabin_w) / 2 - 2.5, H_hull + 7))

    cabin_obj = doc.addObject("Part::Feature", "Cabin")
    cabin_obj.Shape = cabin.cut(window1).cut(window2)

    # 3. Chimney
    chimney_r = 3.5
    chimney_h = 13.0
    chimney = Part.makeCylinder(chimney_r, chimney_h)
    chimney.translate(FreeCAD.Vector(22, W / 2, H_hull + cabin_h))

    chimney_obj = doc.addObject("Part::Feature", "Chimney")
    chimney_obj.Shape = chimney

    # Fusion
    fusion = doc.addObject("Part::MultiFuse", "BenchyBody")
    fusion.Shapes = [hull_obj, cabin_obj, chimney_obj]

    doc.recompute()

    # Ensure output directory exists
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save files to output directory
    doc_path = os.path.abspath(os.path.join(output_dir, "benchy.FCStd"))
    doc.saveAs(doc_path)

    stl_path = os.path.abspath(os.path.join(output_dir, "benchy.stl"))
    Mesh.export([fusion], stl_path)

    # Also save to root directory as per GEMINI.md
    import shutil
    shutil.copy2(doc_path, "benchy.FCStd")
    shutil.copy2(stl_path, "benchy.stl")

    print(f"Benchy model saved to {doc_path} and root.")
    print(f"Benchy STL exported to {stl_path} and root.")
    return doc

if __name__ == "__main__":
    draw_benchy()
