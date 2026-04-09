import sys
import os
import random

# Add FreeCAD to path
from freecad_utils import setup_freecad
if not setup_freecad():
    print("FreeCAD not found.")
    sys.exit(1)

import FreeCAD
import Part
import TechDraw

def export_views(fcstd_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    doc = FreeCAD.openDocument(fcstd_path)
    benchy = doc.getObject("Benchy_Model")
    shape = benchy.Shape

    # Standard Views
    views = {
        "top": FreeCAD.Vector(0, 0, 1),
        "front": FreeCAD.Vector(0, -1, 0),
        "side": FreeCAD.Vector(1, 0, 0)
    }

    html_content = "<html><body><h1>Benchy Report</h1>"

    for name, direction in views.items():
        svg = TechDraw.projectToSVG(shape, direction)
        svg_path = os.path.join(output_dir, f"view_{name}.svg")
        with open(svg_path, "w") as f:
            f.write(svg)
        html_content += f"<h2>{name.capitalize()} View</h2><img src='view_{name}.svg' width='400'><br>"

        # DXF export (TechDraw.projectToDXF returns content as well)
        dxf = TechDraw.projectToDXF(shape, direction)
        dxf_path = os.path.join(output_dir, f"view_{name}.dxf")
        with open(dxf_path, "w") as f:
            f.write(dxf)

    # 6 Random Views
    html_content += "<h1>Random Views</h1>"
    for i in range(1, 7):
        # Random direction
        rx = random.uniform(-1, 1)
        ry = random.uniform(-1, 1)
        rz = random.uniform(-1, 1)
        direction = FreeCAD.Vector(rx, ry, rz).normalize()

        svg = TechDraw.projectToSVG(shape, direction)
        svg_path = os.path.join(output_dir, f"random_{i}.svg")
        with open(svg_path, "w") as f:
            f.write(svg)
        html_content += f"<h3>Random {i}</h3><img src='random_{i}.svg' width='300'> "
        if i % 2 == 0: html_content += "<br>"

    html_content += "</body></html>"

    report_path = os.path.join(output_dir, "report.html")
    with open(report_path, "w") as f:
        f.write(html_content)

    print(f"Report and views generated in {output_dir}")

if __name__ == "__main__":
    export_views("output/benchy.FCStd", "output")
