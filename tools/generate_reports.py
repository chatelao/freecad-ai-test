import sys
import os
import random

sys.path.append(os.path.dirname(__file__))
import freecad_utils

if not freecad_utils.setup_freecad():
    sys.exit(1)

import FreeCAD
import Part
import TechDraw

def generate_reports(fcstd_path, output_dir):
    doc = FreeCAD.open(fcstd_path)
    benchy_obj = doc.getObject("Benchy")
    shape = benchy_obj.Shape

    # 1. Export SVG views (Top, Front, Side)
    views = {
        "top": (0, 0, 1),
        "front": (0, -1, 0),
        "side": (1, 0, 0)
    }

    for name, direction in views.items():
        svg_path = os.path.join(output_dir, f"view_{name}.svg")
        freecad_utils.export_svg(shape, svg_path, direction)

    # 2. 6 Random Views (Simulated by different projections)
    for i in range(6):
        direction = (random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1))
        svg_path = os.path.join(output_dir, f"random_view_{i+1}.svg")
        freecad_utils.export_svg(shape, svg_path, direction)

    print(f"Reports generated in {output_dir}")

if __name__ == "__main__":
    fcstd_path = "output/benchy_temp.FCStd"
    output_dir = "output"
    generate_reports(fcstd_path, output_dir)
