import os
import sys
import argparse

# Add tools directory to path to import freecad_utils
sys.path.append(os.path.join(os.path.dirname(__file__), 'tools'))
import freecad_utils

if not freecad_utils.setup_freecad_path():
    print("Error: Could not find FreeCAD library.")
    sys.exit(1)

import FreeCAD
import TechDraw

def generate_reports(fcstd_path):
    doc = FreeCAD.open(fcstd_path)
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    model = doc.getObject('Benchy')
    if not model:
        print("Error: Could not find model object 'Benchy'.")
        return

    views = {
        "front": FreeCAD.Vector(0, -1, 0),
        "side": FreeCAD.Vector(-1, 0, 0),
        "top": FreeCAD.Vector(0, 0, 1)
    }

    for view_name, direction in views.items():
        svg_filename = os.path.join(output_dir, f"benchy_{view_name}.svg")

        # Use projectToSVG which returns the SVG content as a string
        try:
            svg_content = TechDraw.projectToSVG(model.Shape, direction)
            with open(svg_filename, "w") as f:
                f.write(svg_content)
            print(f"Exported {view_name} view to {svg_filename}")
        except Exception as e:
            print(f"Error projecting {view_name} view to SVG: {e}")

    doc.save()
    return

if __name__ == "__main__":
    fcstd_path = "benchy.FCStd"
    if len(sys.argv) > 1:
        fcstd_path = sys.argv[1]

    generate_reports(fcstd_path)
