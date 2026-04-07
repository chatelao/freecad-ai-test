import sys
import os
import math

def find_freecad():
    # Common paths on Linux
    paths = [
        '/usr/lib/freecad-python3/lib',
        '/usr/lib/freecad/lib',
        '/usr/local/lib/freecad/lib'
    ]

    # Also check environment variable
    if 'FREECADPATH' in os.environ:
        paths.insert(0, os.environ['FREECADPATH'])

    for path in paths:
        if os.path.exists(os.path.join(path, 'FreeCAD.so')):
            return path
    return None

FREECADPATH = find_freecad()
if not FREECADPATH:
    print("Error: Could not find FreeCAD library.")
    sys.exit(1)

sys.path.append(FREECADPATH)

try:
    import FreeCAD
    import Part
    import Mesh
except ImportError as e:
    print(f"Error: {e}")
    sys.exit(1)

def create_benchy():
    # Hull
    # Dimensions: 60mm length, 31mm width, 15.5mm (deck height)
    # Using a simplified loft for the hull

    # Bottom plate (simplified)
    # Stern is at X=-30, Bow is at X=30
    # dX for 40 deg overhang over 15.5mm: 15.5 / tan(40) = 18.47
    # Bow at z=0: X = 30 - 18.47 = 11.53
    p1_pts = [
        FreeCAD.Base.Vector(-20, -5, 0),
        FreeCAD.Base.Vector(-20, 5, 0),
        FreeCAD.Base.Vector(10, 5, 0),
        FreeCAD.Base.Vector(11.53, 0, 0), # Bow point
        FreeCAD.Base.Vector(10, -5, 0),
        FreeCAD.Base.Vector(-20, -5, 0)
    ]
    p1 = Part.makePolygon(p1_pts)

    # Profile 2: Mid-hull (at z=8)
    # Bow at z=8: X = 11.53 + 8 / tan(40) = 11.53 + 9.53 = 21.06
    p2_pts = [
        FreeCAD.Base.Vector(-25, -12, 8),
        FreeCAD.Base.Vector(-25, 12, 8),
        FreeCAD.Base.Vector(10, 12, 8),
        FreeCAD.Base.Vector(21.06, 0, 8), # Bow point
        FreeCAD.Base.Vector(10, -12, 8),
        FreeCAD.Base.Vector(-25, -12, 8)
    ]
    p2 = Part.makePolygon(p2_pts)

    # Profile 3: Deck (at z=15.5)
    # Bow at z=15.5: X = 30
    p3_pts = [
        FreeCAD.Base.Vector(-30, -15.5, 15.5),
        FreeCAD.Base.Vector(-30, 15.5, 15.5),
        FreeCAD.Base.Vector(10, 15.5, 15.5),
        FreeCAD.Base.Vector(30, 0, 15.5), # Bow point
        FreeCAD.Base.Vector(10, -15.5, 15.5),
        FreeCAD.Base.Vector(-30, -15.5, 15.5)
    ]
    p3 = Part.makePolygon(p3_pts)

    hull = Part.makeLoft([p1, p2, p3], True)

    # Cargo Box on Deck
    # Outside: 12.00 x 10.81 mm. Inside: 8.00 x 7.00 mm. Depth: 9.00 mm.
    cargo_outer = Part.makeBox(12.00, 10.81, 9.00)
    cargo_outer.translate(FreeCAD.Base.Vector(10, -5.405, 15.5))

    cargo_inner = Part.makeBox(8.00, 7.00, 10.00)
    cargo_inner.translate(FreeCAD.Base.Vector(12, -3.5, 16.5))

    cargo_box = cargo_outer.cut(cargo_inner)

    # Cabin (Bridge)
    # Total Height: 48mm. Deck: 15.5mm.
    cabin_main = Part.makeBox(20, 20, 25)
    cabin_main.translate(FreeCAD.Base.Vector(-15, -10, 15.5))

    # Windows
    front_window = Part.makeBox(2, 10.5, 9.5)
    front_window.translate(FreeCAD.Base.Vector(4, -5.25, 25))
    cabin_hollow = cabin_main.cut(front_window)

    # Roof with inclination
    # Roof is 23mm long according to specs.
    roof_box = Part.makeBox(23, 25, 2)
    roof_box.translate(FreeCAD.Base.Vector(-16.5, -12.5, 40.5))
    # Inclination 5.5 deg around Y axis at the front (X=6.5)
    roof_box.rotate(FreeCAD.Base.Vector(6.5, 0, 40.5), FreeCAD.Base.Vector(0, 1, 0), -5.5)

    # Chimney
    # Outer: 7mm dia, Inner: 3mm dia, Depth: 11mm.
    # Total height 48mm. Top should be at 48.
    chimney_height = 48 - 40.5
    chimney_outer = Part.makeCylinder(3.5, chimney_height)
    chimney_outer.translate(FreeCAD.Base.Vector(-5, 0, 40.5))

    chimney_inner = Part.makeCylinder(1.5, 11)
    chimney_inner.translate(FreeCAD.Base.Vector(-5, 0, 48 - 11))

    chimney = chimney_outer.cut(chimney_inner)

    # Combine everything
    benchy = Part.Compound([hull, cargo_box, cabin_hollow, roof_box, chimney])

    return benchy

def main():
    benchy_shape = create_benchy()
    print(f"Shape BoundBox: {benchy_shape.BoundBox}")

    # Export to STL
    mesh = Mesh.Mesh()
    mesh.addFacets(benchy_shape.tessellate(0.1))
    mesh.write("benchy.stl")
    print("Benchy model exported to benchy.stl")

if __name__ == "__main__":
    main()
