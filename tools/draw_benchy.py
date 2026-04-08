import sys
import os
import math

# Add the tools directory to sys.path so we can import freecad_utils
sys.path.append(os.path.dirname(__file__))
import freecad_utils

if not freecad_utils.setup_freecad():
    sys.exit(1)

import FreeCAD
import Part

def create_benchy():
    doc = FreeCAD.newDocument("Benchy")

    # Dimensions
    length = 60.0 # X axis
    width = 31.0  # Y axis
    height = 48.0 # Z axis (total target)
    deck_height = 15.5
    bow_angle = 40.0
    roof_angle = 5.5
    roof_length = 23.0

    # 1. Hull
    # Base hull box
    hull_box = Part.makeBox(length, width, deck_height)

    # Bow Overhang (40 degrees) at +X
    # We want the front face to be angled.
    # The height is 15.5. The horizontal offset for 40 degrees is 15.5 / tan(40)
    offset = deck_height / math.tan(math.radians(bow_angle))

    # Create a wedge-like cutter for the bow
    # We use a large box and rotate it
    bow_cutter = Part.makeBox(offset * 2, width + 10, deck_height * 2)
    bow_cutter.translate(FreeCAD.Vector(-offset * 2, -5, 0))
    bow_cutter.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), 90 - bow_angle)
    bow_cutter.translate(FreeCAD.Vector(length, 0, 0))

    hull = hull_box.cut(bow_cutter)

    # Round the hull sides (Simplified as a chamfer/fillet logic in a real CAD, here we'll use a wedge cutter)
    # For simplicity in this script, we'll keep the side walls vertical for now but ensure dimensions.
    hull.translate(FreeCAD.Vector(-length/2, -width/2, 0))

    # 2. Hawsepipes (Holes in the bow)
    hawse_radius = 2.0
    hawse_pipe_r = Part.makeCylinder(hawse_radius, 10)
    hawse_pipe_r.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,1,0), 90)
    hawse_pipe_r.translate(FreeCAD.Vector(length/2 - 5, width/2 - 5, deck_height - 5))

    hawse_pipe_l = Part.makeCylinder(hawse_radius, 10)
    hawse_pipe_l.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,1,0), 90)
    hawse_pipe_l.translate(FreeCAD.Vector(length/2 - 5, -width/2 + 5, deck_height - 5))

    hull = hull.cut(hawse_pipe_r).cut(hawse_pipe_l)

    # 3. Deck
    deck = Part.makeBox(length, width, 1)
    deck.translate(FreeCAD.Vector(-length/2, -width/2, deck_height - 1))

    # 4. Cargo Box
    cargo_outer_l = 12.0
    cargo_outer_w = 10.81
    cargo_outer = Part.makeBox(cargo_outer_l, cargo_outer_w, 9.0)
    cargo_outer.translate(FreeCAD.Vector(-length/4, -cargo_outer_w/2, deck_height))

    cargo_inner_l = 8.0
    cargo_inner_w = 7.0
    cargo_inner = Part.makeBox(cargo_inner_l, cargo_inner_w, 9.0)
    cargo_inner.translate(FreeCAD.Vector(-length/4 + (cargo_outer_l - cargo_inner_l)/2, -cargo_inner_w/2, deck_height + 1))
    cargo_box = cargo_outer.cut(cargo_inner)

    # 5. Bridge (Cabin)
    bridge_l = 18.0
    bridge_w = 15.0
    bridge_h = 15.0
    bridge = Part.makeBox(bridge_l, bridge_w, bridge_h)
    bridge.translate(FreeCAD.Vector(0, -bridge_w/2, deck_height))

    # Front Window (Rectangular 10.5 x 9.5)
    window_front = Part.makeBox(5.0, 10.5, 9.5)
    window_front.translate(FreeCAD.Vector(bridge_l - 2, -10.5/2, deck_height + 3))
    bridge = bridge.cut(window_front)

    # Rear Window (Cylindrical Diameter 9)
    window_rear = Part.makeCylinder(4.5, 5.0)
    window_rear.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,1,0), 90)
    window_rear.translate(FreeCAD.Vector(-2, 0, deck_height + 7))
    bridge = bridge.cut(window_rear)

    # 6. Roof
    roof_w = bridge_w + 4
    roof = Part.makeBox(roof_length, roof_w, 2)
    # The roof should be centered over the bridge.
    roof.translate(FreeCAD.Vector((bridge_l - roof_length)/2, -roof_w/2, deck_height + bridge_h))
    # Apply roof angle (5.5 degrees) - Rotating around Y axis at the front of the roof
    roof.rotate(FreeCAD.Vector(bridge_l/2 + roof_length/2, 0, deck_height + bridge_h), FreeCAD.Vector(0, 1, 0), -roof_angle)

    # 7. Chimney
    chimney_h = 48.0 - (deck_height + bridge_h)
    chimney_outer = Part.makeCylinder(3.5, chimney_h)
    chimney_outer.translate(FreeCAD.Vector(bridge_l/2, 0, deck_height + bridge_h))
    chimney_inner = Part.makeCylinder(1.5, 11.0)
    chimney_inner.translate(FreeCAD.Vector(bridge_l/2, 0, deck_height + bridge_h + (chimney_h - 11)))
    chimney = chimney_outer.cut(chimney_inner)

    # 8. Stern Nameplate
    nameplate = Part.makeBox(0.1, 15, 5)
    nameplate.translate(FreeCAD.Vector(-length/2, -7.5, deck_height - 7))

    # Combine all parts
    benchy = hull.fuse(deck).fuse(cargo_box).fuse(bridge).fuse(roof).fuse(chimney).fuse(nameplate)

    # Add to document
    obj = doc.addObject("Part::Feature", "Benchy")
    obj.Shape = benchy

    doc.recompute()
    return doc, obj

if __name__ == "__main__":
    doc, benchy_obj = create_benchy()
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save FCStd
    fcstd_path = os.path.join(output_dir, "benchy_temp.FCStd")
    doc.saveAs(fcstd_path)
    print(f"Saved FreeCAD document to {fcstd_path}")

    # Export STL
    stl_path = os.path.join(output_dir, "benchy_temp.stl")
    freecad_utils.export_stl(doc, stl_path)
