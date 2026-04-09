import sys
import os

# Setup FreeCAD path
def setup_freecad():
    paths = [
        os.environ.get("FREECADPATH"),
        "/usr/lib/freecad-python3/lib",
        "/usr/lib/freecad/lib",
        "/usr/local/lib/freecad/lib"
    ]
    for p in paths:
        if p and os.path.exists(p):
            if p not in sys.path:
                sys.path.append(p)
            return True
    return False

setup_freecad()

import FreeCAD as App
import Part
import Mesh

def create_benchy():
    doc = App.newDocument("Benchy")

    # 1. Hull
    hull = Part.makeBox(60, 31, 15)
    cutter_l = Part.makePolygon([App.Vector(30,0,-1), App.Vector(61,-10,-1), App.Vector(61,15.5,-1), App.Vector(30,0,-1)])
    cutter_l_face = Part.Face(cutter_l)
    cutter_l_vol = cutter_l_face.extrude(App.Vector(0,0,17))

    cutter_r = Part.makePolygon([App.Vector(30,31,-1), App.Vector(61,41,-1), App.Vector(61,15.5,-1), App.Vector(30,31,-1)])
    cutter_r_face = Part.Face(cutter_r)
    cutter_r_vol = cutter_r_face.extrude(App.Vector(0,0,17))

    hull = hull.cut(cutter_l_vol).cut(cutter_r_vol)

    # 2. Deck
    deck_recess = Part.makeBox(50, 27, 5, App.Vector(2, 2, 12))
    hull = hull.cut(deck_recess)

    # 3. Cabin
    cabin = Part.makeBox(20, 20, 20, App.Vector(15, 5.5, 12))
    window_f = Part.makeBox(2, 12, 10, App.Vector(34, 9.5, 18))
    cabin = cabin.cut(window_f)

    # 4. Chimney
    chimney = Part.makeCylinder(3.5, 15, App.Vector(28, 15.5, 32))
    chimney_hole = Part.makeCylinder(1.5, 16, App.Vector(28, 15.5, 32))
    chimney = chimney.cut(chimney_hole)

    benchy = hull.fuse(cabin).fuse(chimney)

    obj = doc.addObject("Part::Feature", "Benchy")
    obj.Shape = benchy

    doc.recompute()

    if not os.path.exists("output"):
        os.makedirs("output")

    doc.saveAs("output/benchy.FCStd")
    mesh = Mesh.Mesh()
    mesh.addFacets(obj.Shape.tessellate(0.1))
    mesh.write("output/benchy.stl")

    print("Benchy generated successfully.")

if __name__ == "__main__":
    create_benchy()
