import os
import sys
import random
from freecad_utils import setup_freecad, wrap_svg

if not setup_freecad():
    print("Error: FreeCAD could not be loaded.")
    sys.exit(1)

import FreeCAD
import Part
import TechDraw

def generate_reports():
    output_dir = "output"
    # Prioritize output/ then root
    fcstd_path = os.path.join(output_dir, "benchy.FCStd")
    if not os.path.exists(fcstd_path):
        fcstd_path = "benchy.FCStd"

    if not os.path.exists(fcstd_path):
        print(f"Error: {fcstd_path} not found. Run draw_benchy.py first.")
        return

    doc = FreeCAD.openDocument(fcstd_path)
    benchy = doc.getObject("Benchy")

    views = {
        "top": FreeCAD.Vector(0, 0, 1),
        "front": FreeCAD.Vector(0, -1, 0),
        "side": FreeCAD.Vector(1, 0, 0)
    }

    for name, direction in views.items():
        # In FreeCAD 0.21, projectToSVG/DXF takes the Shape
        svg_content = TechDraw.projectToSVG(benchy.Shape, direction)
        svg_content = wrap_svg(svg_content)
        svg_path = os.path.join(output_dir, f"benchy_{name}.svg")
        with open(svg_path, "w") as f:
            f.write(svg_content)
        print(f"Generated {svg_path}")

        dxf_content = TechDraw.projectToDXF(benchy.Shape, direction)
        dxf_path = os.path.join(output_dir, f"benchy_{name}.dxf")
        with open(dxf_path, "w") as f:
            f.write(dxf_content)
        print(f"Generated {dxf_path}")

    # 6 Random views
    for i in range(6):
        rand_dir = FreeCAD.Vector(random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1))
        if rand_dir.Length < 0.1: rand_dir = FreeCAD.Vector(1,1,1)
        rand_dir.normalize()

        svg_content = TechDraw.projectToSVG(benchy.Shape, rand_dir)
        svg_content = wrap_svg(svg_content)
        svg_path = os.path.join(output_dir, f"benchy_random_{i}.svg")
        with open(svg_path, "w") as f:
            f.write(svg_content)
        print(f"Generated {svg_path}")

    html_content = f"""
    <html>
    <head><title>3DBenchy Report</title></head>
    <body>
    <h1>3DBenchy Report</h1>
    <h2>Standard Views</h2>
    <div style="display: flex;">
        <div><h3>Top</h3><img src="benchy_top.svg" width="300"></div>
        <div><h3>Front</h3><img src="benchy_front.svg" width="300"></div>
        <div><h3>Side</h3><img src="benchy_side.svg" width="300"></div>
    </div>
    <h2>Random Views</h2>
    <div style="display: grid; grid-template-columns: repeat(3, 1fr);">
    """
    for i in range(6):
        html_content += f'<div><img src="benchy_random_{i}.svg" width="200"></div>\n'
    html_content += "</div></body></html>"

    html_path = os.path.join(output_dir, "report.html")
    with open(html_path, "w") as f:
        f.write(html_content)
    print(f"Generated {html_path}")

if __name__ == "__main__":
    generate_reports()
