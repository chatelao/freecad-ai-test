import sys
import os

# Setup FreeCAD path
from freecad_utils import setup_freecad
if not setup_freecad():
    print("FreeCAD library not found!")
    sys.exit(1)

import FreeCAD
import Part
import TechDraw

def generate_reports(fcstd_path):
    if not os.path.exists(fcstd_path):
        print(f"File not found: {fcstd_path}")
        return

    doc = FreeCAD.openDocument(fcstd_path)

    # Create a compound of all objects to project
    shapes = []
    for obj in doc.Objects:
        if hasattr(obj, "Shape"):
            shapes.append(obj.Shape)

    combined_shape = Part.makeCompound(shapes)

    views = {
        "top": FreeCAD.Vector(0, 0, 1),
        "front": FreeCAD.Vector(0, -1, 0),
        "side": FreeCAD.Vector(1, 0, 0)
    }

    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    html_content = "<html><body><h1>Benchy Report</h1>"

    for name, direction in views.items():
        print(f"Projecting {name} view...")

        # SVG
        svg_content = TechDraw.projectToSVG(combined_shape, direction)
        svg_path = os.path.join(output_dir, f"benchy_{name}.svg")
        with open(svg_path, "w") as f:
            f.write(svg_content)
        print(f"  Saved {svg_path}")

        # DXF
        dxf_content = TechDraw.projectToDXF(combined_shape, direction)
        dxf_path = os.path.join(output_dir, f"benchy_{name}.dxf")
        with open(dxf_path, "w") as f:
            f.write(dxf_content)
        print(f"  Saved {dxf_path}")

        html_content += f"<h2>{name.capitalize()} View</h2>"
        html_content += f'<img src="benchy_{name}.svg" width="400"><br>'

    html_content += "</body></html>"
    report_html = os.path.join(output_dir, "report.html")
    with open(report_html, "w") as f:
        f.write(html_content)

    print(f"Report HTML saved to {report_html}")

    # Note: PDF export might need external tools or TechDraw Page export
    # For this environment, we provide the HTML and SVG views.

if __name__ == "__main__":
    fcstd_file = "benchy.FCStd"
    generate_reports(fcstd_file)
