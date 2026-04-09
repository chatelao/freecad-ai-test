import os
import sys
import random

# Setup FreeCAD path
from freecad_utils import setup_freecad, ensure_output_dir
if not setup_freecad():
    sys.exit(1)

import FreeCAD
import Part
import TechDraw

def fix_svg(svg_content):
    """Adds XML header and ensures valid SVG structure."""
    if not svg_content.startswith("<?xml"):
        header = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
        # Basic SVG wrapper if needed, though TechDraw usually provides it.
        # But projectToSVG returns just the inner content sometimes.
        if "<svg" not in svg_content:
             svg_content = f'{header}<svg xmlns="http://www.w3.org/2000/svg" version="1.1">\n{svg_content}\n</svg>'
        else:
             svg_content = header + svg_content
    return svg_content

def export_views(obj, name_prefix):
    """Exports top, front, and side views as SVG and DXF."""
    views = {
        "top": FreeCAD.Vector(0, 0, 1),
        "front": FreeCAD.Vector(0, -1, 0),
        "side": FreeCAD.Vector(1, 0, 0)
    }

    for view_name, direction in views.items():
        # Export SVG
        svg_file = f"output/{name_prefix}_{view_name}.svg"
        svg_content = TechDraw.projectToSVG(obj.Shape, direction)
        with open(svg_file, "w") as f:
            f.write(fix_svg(svg_content))

        # Export DXF
        dxf_file = f"output/{name_prefix}_{view_name}.dxf"
        dxf_content = TechDraw.projectToDXF(obj.Shape, direction)
        with open(dxf_file, "w") as f:
            f.write(dxf_content)

        print(f"Exported {view_name} view for {name_prefix}")

def render_random_views(obj, count=6):
    """Renders random views of the model."""
    for i in range(count):
        direction = FreeCAD.Vector(random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1))
        direction.normalize()
        svg_file = f"output/random_view_{i+1}.svg"
        svg_content = TechDraw.projectToSVG(obj.Shape, direction)
        with open(svg_file, "w") as f:
            f.write(fix_svg(svg_content))
        print(f"Rendered random view {i+1}")

def main():
    ensure_output_dir()
    doc = FreeCAD.open("output/benchy.FCStd")
    benchy_obj = doc.getObject("Benchy")

    if not benchy_obj:
        print("Error: Benchy object not found in FCStd file.")
        return

    export_views(benchy_obj, "benchy")
    render_random_views(benchy_obj)

    # Generate a simple HTML report as a fallback for PDF
    html_content = "<html><body><h1>Benchy Report</h1>"
    for view in ["top", "front", "side"]:
        html_content += f"<h2>{view.capitalize()} View</h2>"
        html_content += f'<img src="benchy_{view}.svg" width="400"><br>'

    html_content += "<h2>Random Views</h2>"
    for i in range(6):
        html_content += f'<img src="random_view_{i+1}.svg" width="200">'

    html_content += "</body></html>"

    with open("output/report.html", "w") as f:
        f.write(html_content)
    print("Report generated in output/report.html")

if __name__ == "__main__":
    main()
