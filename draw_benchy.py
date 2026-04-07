import sys
import os

# Set FreeCAD path
FREECADPATH = '/usr/lib/freecad-python3/lib'
if FREECADPATH not in sys.path:
    sys.path.append(FREECADPATH)

try:
    import FreeCAD
    import Part
    import Mesh
except ImportError as e:
    print(f"Error: {e}")
    sys.exit(1)

def create_benchy():
    doc = FreeCAD.newDocument("Benchy")

    # 1. Hull
    # Dimensions: 60mm long, 31mm wide
    # We'll use a more refined hull shape: lofting between several cross-sections.

    # Bottom plate (at Z=0) - thin ellipse/oval
    wire1 = Part.makePolygon([
        FreeCAD.Vector(0, 0, 0),
        FreeCAD.Vector(20, 8, 0),
        FreeCAD.Vector(45, 10, 0),
        FreeCAD.Vector(60, 0, 0), # Bow
        FreeCAD.Vector(45, -10, 0),
        FreeCAD.Vector(20, -8, 0),
        FreeCAD.Vector(0, 0, 0)
    ])

    # Middle section (at Z=10) - wider
    wire2 = Part.makePolygon([
        FreeCAD.Vector(-2, 0, 10),
        FreeCAD.Vector(20, 14, 10),
        FreeCAD.Vector(45, 15.5, 10),
        FreeCAD.Vector(62, 0, 10),
        FreeCAD.Vector(45, -15.5, 10),
        FreeCAD.Vector(20, -14, 10),
        FreeCAD.Vector(-2, 0, 10)
    ])

    # Top deck level (at Z=15.5) - deck shape
    wire3 = Part.makePolygon([
        FreeCAD.Vector(-5, 0, 15.5),
        FreeCAD.Vector(20, 15.5, 15.5),
        FreeCAD.Vector(45, 15.5, 15.5),
        FreeCAD.Vector(65, 0, 15.5),
        FreeCAD.Vector(45, -15.5, 15.5),
        FreeCAD.Vector(20, -15.5, 15.5),
        FreeCAD.Vector(-5, 0, 15.5)
    ])

    hull_loft = Part.makeLoft([wire1, wire2, wire3], True)
    hull_obj = doc.addObject("Part::Feature", "Hull")
    hull_obj.Shape = hull_loft

    # 2. Deck and Box
    # Cargo-box: 12 x 10.81 outside, 8 x 7 inside, 9 deep.
    # Top of box is 15.5mm above bottom.
    box_outer = Part.makeBox(12, 10.81, 9)
    # Position it near the stern (rear)
    box_outer.translate(FreeCAD.Vector(5, -5.405, 15.5 - 9))

    box_inner = Part.makeBox(8, 7, 10)
    box_inner.translate(FreeCAD.Vector(7, -3.5, 15.5 - 9 + 1))

    cargo_box = box_outer.cut(box_inner)
    cargo_box_obj = doc.addObject("Part::Feature", "CargoBox")
    cargo_box_obj.Shape = cargo_box

    # 3. Cabin (Bridge)
    # Bridge roof length: 23mm.
    cabin_base = Part.makeBox(20, 18, 15)
    cabin_base.translate(FreeCAD.Vector(25, -9, 15.5))

    # Cabin Windows (front)
    window_front = Part.makeBox(1, 10.5, 9.5)
    window_front.translate(FreeCAD.Vector(44, -5.25, 18))

    # Cabin Windows (rear) - circular 9mm
    window_rear = Part.makeCylinder(4.5, 5)
    window_rear.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,1,0), 90)
    window_rear.translate(FreeCAD.Vector(22, 0, 22))

    cabin = cabin_base.cut(window_front).cut(window_rear)
    cabin_obj = doc.addObject("Part::Feature", "Cabin")
    cabin_obj.Shape = cabin

    # 4. Roof
    # Bridge roof inclination: 5.5°
    roof = Part.makeBox(23, 22, 2)
    roof.translate(FreeCAD.Vector(23, -11, 30.5))
    roof.rotate(FreeCAD.Vector(45, 0, 30.5), FreeCAD.Vector(0, 1, 0), -5.5)
    roof_obj = doc.addObject("Part::Feature", "Roof")
    roof_obj.Shape = roof

    # 5. Chimney
    # 7mm outer, 3mm inner, 11mm deep
    chimney_outer = Part.makeCylinder(3.5, 11)
    chimney_inner = Part.makeCylinder(1.5, 12)
    chimney = chimney_outer.cut(chimney_inner)
    chimney.translate(FreeCAD.Vector(35, 0, 32)) # on top of the roof
    chimney_obj = doc.addObject("Part::Feature", "Chimney")
    chimney_obj.Shape = chimney

    # 6. Hawsepipe
    # 4mm inner diameter
    hawsepipe_l = Part.makeCylinder(2, 10)
    hawsepipe_l.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,1,0), 90)
    hawsepipe_l.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,0,1), 150)
    hawsepipe_l.translate(FreeCAD.Vector(55, 5, 10))

    hawsepipe_r = Part.makeCylinder(2, 10)
    hawsepipe_r.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,1,0), 90)
    hawsepipe_r.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,0,1), -150)
    hawsepipe_r.translate(FreeCAD.Vector(55, -5, 10))

    hawse_obj_l = doc.addObject("Part::Feature", "HawsepipeL")
    hawse_obj_l.Shape = hawsepipe_l
    hawse_obj_r = doc.addObject("Part::Feature", "HawsepipeR")
    hawse_obj_r.Shape = hawsepipe_r

    # 7. Nameplate
    # Extruded at 0.10 mm
    nameplate = Part.makeBox(0.1, 15, 5)
    nameplate.translate(FreeCAD.Vector(-5.1, -7.5, 5))
    nameplate_obj = doc.addObject("Part::Feature", "Nameplate")
    nameplate_obj.Shape = nameplate

    doc.recompute()

    # Save
    doc.saveAs("benchy.FCStd")

    # Export STL - Including all objects now
    all_objs = [hull_obj, cargo_box_obj, cabin_obj, roof_obj, chimney_obj, hawse_obj_l, hawse_obj_r, nameplate_obj]
    Mesh.export(all_objs, "benchy.stl")

    print("Benchy model 'benchy.FCStd' and 'benchy.stl' have been updated with feedback.")

if __name__ == "__main__":
    create_benchy()
