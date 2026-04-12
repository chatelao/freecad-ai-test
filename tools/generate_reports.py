import sys
import os
import random

from freecad_utils import setup_freecad, get_template_path
setup_freecad()

import FreeCAD as App
import Part

def generate_reports():
    fcstd_path = "output/benchy.FCStd"
    if not os.path.exists(fcstd_path):
        print(f"File not found: {fcstd_path}")
        return

    doc = App.open(fcstd_path)
    benchy_obj = doc.ActiveObject
    shape = benchy_obj.Shape

    # Try importing TechDraw inside
    try:
        import TechDraw
    except ImportError:
        print("TechDraw not available.")
        return

    views = [
        ("top", App.Vector(0,0,1)),
        ("front", App.Vector(0,1,0)),
        ("side", App.Vector(1,0,0))
    ]

    for i in range(6):
        dx = random.uniform(-1, 1)
        dy = random.uniform(-1, 1)
        dz = random.uniform(-1, 1)
        views.append((f"random_{i+1}", App.Vector(dx, dy, dz)))

    svg_files = []
    for name, direction in views:
        try:
            svg_content = TechDraw.projectToSVG(shape, direction)
            filename = f"output/{name}_view.svg"
            with open(filename, "w") as f:
                f.write(svg_content)
            svg_files.append(filename)
        except Exception as e:
            print(f"Error for {name}: {e}")

    # Since PDF generation is failing due to missing system dependencies for pycairo/rsvg-convert,
    # we will provide the SVGs as the primary report format for now, as they satisfy the
    # "Export files for each the top, front and the side view" and random views requirements.
    # We will also create an HTML report that embeds all SVGs.

    try:
        html_content = "<html><body><h1>3DBenchy Report</h1>"
        for svg_file in svg_files:
            name = os.path.basename(svg_file)
            html_content += f"<h3>{name}</h3><img src='{name}' /><br/>"
        html_content += "</body></html>"
        with open("output/report.html", "w") as f:
            f.write(html_content)
        print("HTML report generated at output/report.html")
    except Exception as e:
        print(f"Could not generate HTML report: {e}")

    print("Generation complete.")

if __name__ == "__main__":
    generate_reports()
