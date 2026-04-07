import sys
import os
from freecad_utils import setup_freecad_path

# Setup FreeCAD path
fc_path = setup_freecad_path()
import FreeCAD
import Part
import Mesh

def create_benchy():
    doc = FreeCAD.newDocument("Benchy")

    # Dimensions
    L = 60.0
    W = 31.0
    H_hull = 15.0
    H_total = 48.0

    # 1. Hull (Simplified as a Box with chamfers for now)
    hull = Part.makeBox(L, W, H_hull)
    hull.translate(FreeCAD.Vector(-L/2, -W/2, 0))

    # Simple bow shaping (cut off corners)
    cut1 = Part.makeBox(L/2, W, H_hull)
    cut1.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,0,1), 45)
    cut1.translate(FreeCAD.Vector(-L/2, W/2, 0))
    hull = hull.cut(cut1)

    cut2 = Part.makeBox(L/2, W, H_hull)
    cut2.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,0,1), -45)
    cut2.translate(FreeCAD.Vector(-L/2, -W/2, 0))
    hull = hull.cut(cut2)

    # 2. Cabin
    cabin_l, cabin_w, cabin_h = 25.0, 20.0, 20.0
    cabin = Part.makeBox(cabin_l, cabin_w, cabin_h)
    cabin.translate(FreeCAD.Vector(-cabin_l/2 + 5, -cabin_w/2, H_hull))

    # 3. Roof (simplified as a box on top of cabin)
    roof_h = 3.0
    roof = Part.makeBox(cabin_l + 4, cabin_w + 4, roof_h)
    roof.translate(FreeCAD.Vector(-cabin_l/2 + 3, -cabin_w/2 - 2, H_hull + cabin_h))

    # 4. Chimney
    chim_r = 4.0
    chim_h = 10.0
    chimney = Part.makeCylinder(chim_r, chim_h)
    chimney.translate(FreeCAD.Vector(0, 0, H_hull + cabin_h + roof_h))

    # Combine all parts
    benchy = hull.fuse(cabin).fuse(roof).fuse(chimney)

    # Add to document
    obj = doc.addObject("Part::Feature", "Benchy")
    obj.Shape = benchy

    doc.recompute()

    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)

    # Export
    doc.saveAs("output/benchy.FCStd")
    Mesh.export([obj], "output/benchy.stl")

    print("Benchy created and exported to output/benchy.FCStd and output/benchy.stl")

if __name__ == "__main__":
    create_benchy()
