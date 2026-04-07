import sys
import os
import math
from freecad_utils import init_freecad

def main():
    FreeCAD = init_freecad()
    if not FreeCAD:
        sys.exit(1)

    import Part
    import Mesh

    # Create a new document
    doc = FreeCAD.newDocument("Benchy")

    # Dimensions (Official Calibration Specifications)
    # Overall dimensions
    total_length = 60.0 # bow to stern
    total_width = 31.0 # port to starboard
    total_height = 48.0 # top to bottom
    hull_h = 15.5 # deck height at stern
    bow_angle = 40.0 # bow overhang angle to horizontal

    # 1. Hull
    # Calculated bow extension (horizontal)
    bow_ext = hull_h / math.tan(math.radians(bow_angle))
    stern_l = total_length - bow_ext

    # Primitive-based Hull (Stern box + Bow wedge)
    stern = Part.makeBox(stern_l, total_width, hull_h)
    stern.translate(FreeCAD.Vector(-total_length/2, -total_width/2, 0))

    bow = Part.makeWedge(0, 0, 0, 0, 0, bow_ext, total_width, hull_h, 0, 0)
    bow.translate(FreeCAD.Vector(-total_length/2 + stern_l, -total_width/2, 0))
    hull = stern.fuse(bow)

    # Hawsepipe (4.00 mm diameter)
    hawse_id = 4.0
    hawse_pipe = Part.makeCylinder(hawse_id/2, total_width + 10)
    hawse_pipe.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(1,0,0), 90)
    hawse_pipe.translate(FreeCAD.Vector(total_length/2 - bow_ext/2, total_width/2 + 5, hull_h - 5))
    hull = hull.cut(hawse_pipe)

    # 2. Cargo Box
    # Outside: 12.00 x 10.81 mm. Inside: 8.00 x 7.00 mm. Depth: 9.00 mm.
    box_o = Part.makeBox(12.00, 10.81, 9.00)
    box_i = Part.makeBox(8.00, 7.00, 9.00)
    box_i.translate(FreeCAD.Vector(2.0, (10.81-7.0)/2, 1.0)) # 1mm bottom
    cargo_box = box_o.cut(box_i)
    cargo_box.translate(FreeCAD.Vector(-total_length/2 + 2, -10.81/2, hull_h))

    # 3. Cabin / Bridge
    # Length: 23.00 mm. Roof inclination: 5.5°.
    cabin_l = 23.00
    cabin_w = 20.00
    # Height calculation: hull_h (15.5) + cabin_h + chimney_h = total_height (48)
    # We want chimney top at 48mm. Chimney is 12.5mm high.
    # So cabin top at chimney base must be 35.5mm.
    # 35.5 - 15.5 (hull) = 20.0mm (cabin height at chimney position)
    cabin_h = 25.0 # use extra height and cut it with tilted roof

    cabin = Part.makeBox(cabin_l, cabin_w, cabin_h)

    # 5.5° Roof Inclination (Slopped from back to front)
    # We want the highest point to be exactly 48mm (at chimney top).
    # Let's say the chimney is centered in X on the cabin.
    # Let's say the chimney is at X=0 (centered in cabin of 23mm length)
    # So X ranges from -11.5 to +11.5
    # Roof height: Z = 48.0 - 12.5 (chimney) - 15.5 (hull) = 20mm at X=0.
    # Inclination 5.5°. Z(x) = 20 + x * tan(5.5°)

    roof_plane_h = 20.0
    roof_cutter = Part.makeBox(cabin_l * 2, cabin_w * 2, 20)
    roof_cutter.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,1,0), -5.5)
    # Positioning so it cuts at height 20 when x=0
    roof_cutter.translate(FreeCAD.Vector(-cabin_l, -cabin_w, roof_plane_h))

    # Adjust for cabin position
    cabin.translate(FreeCAD.Vector(-cabin_l/2, -cabin_w/2, hull_h))
    cabin = cabin.cut(roof_cutter)

    # Cabin Windows
    # Front: 10.50 x 9.50 mm (rectangular)
    win_f = Part.makeBox(5.0, 10.50, 9.50)
    win_f.translate(FreeCAD.Vector(cabin_l/2 - 2, -10.50/2, hull_h + 5.0))
    cabin = cabin.cut(win_f)

    # Rear (Stern): 9.00 mm inner diameter (cylindrical)
    win_r = Part.makeCylinder(4.5, 5.0)
    win_r.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,1,0), 90)
    win_r.translate(FreeCAD.Vector(-cabin_l/2 - 2, 0, hull_h + 10.0))
    cabin = cabin.cut(win_r)

    # 4. Chimney
    # Outer: 7.00 mm. Inner: 3.00 mm. Blind hole depth: 11.00 mm.
    chimney_h = 12.5
    chim_o = Part.makeCylinder(3.5, chimney_h)
    chim_i = Part.makeCylinder(1.5, 11.0) # 11mm depth
    chim_i.translate(FreeCAD.Vector(0, 0, chimney_h - 11.0))
    chimney = chim_o.cut(chim_i)
    # Position: Centered on the cabin roof (X=0)
    chimney.translate(FreeCAD.Vector(0, 0, hull_h + roof_plane_h))

    # 5. Stern Nameplate (0.1mm extrusion)
    # Plate is 0.1mm, we need to subtract it from the hull length or place it carefully.
    # Total length 60.0. Hull stern is at -30.0. Plate is at -30.0 to -30.1.
    # To keep total length at 60.0, we can subtract 0.1 from the stern length or keep it as is if 0.1 tolerance is okay.
    plate = Part.makeBox(0.1, 15.0, 5.0)
    plate.translate(FreeCAD.Vector(-total_length/2, -7.5, hull_h - 10.0))

    # --- Final Construction ---
    benchy_shape = hull.fuse(cargo_box).fuse(cabin).fuse(chimney).fuse(plate)

    final_obj = doc.addObject("Part::Feature", "BenchyBody")
    final_obj.Shape = benchy_shape

    doc.recompute()

    # Save and Export
    os.makedirs("output", exist_ok=True)
    doc.saveAs("output/benchy.FCStd")
    Mesh.export([final_obj], "output/benchy.stl")
    print("Benchy generated with detailed features (Windows, Roof Slope, Hawsepipe, Nameplate).")

if __name__ == "__main__":
    main()
