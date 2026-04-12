import sys
import os
import subprocess

# Setup FreeCAD path
def setup_freecad():
    paths = [
        os.environ.get("FREECADPATH"),
        "/usr/lib/freecad-python3/lib",
        "/usr/lib/freecad/lib",
        "/usr/local/lib/freecad/lib"
    ]
    for p in paths:
        if p and os.path.exists(p):
            if p not in sys.path:
                sys.path.append(p)
            return True
    return False

setup_freecad()

import FreeCAD as App
import Part
import TechDraw

def generate_reports():
    doc = App.openDocument("output/benchy.FCStd")
    obj = doc.getObject("Benchy")

    views = {
        "top": App.Vector(0, 0, 1),
        "front": App.Vector(0, -1, 0),
        "side": App.Vector(-1, 0, 0)
    }

    svg_files = []
    for name, direction in views.items():
        # SVG
        svg_content = TechDraw.projectToSVG(obj.Shape, direction)
        if not svg_content.startswith("<?xml"):
            full_svg = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
            full_svg += '<svg xmlns="http://www.w3.org/2000/svg" version="1.1">\n'
            full_svg += svg_content
            full_svg += "\n</svg>"
        else:
            full_svg = svg_content

        svg_path = f"output/benchy_{name}.svg"
        with open(svg_path, "w") as f:
            f.write(full_svg)
        svg_files.append(svg_path)

        # DXF
        dxf_content = TechDraw.projectToDXF(obj.Shape, direction)
        with open(f"output/benchy_{name}.dxf", "w") as f:
            f.write(dxf_content)

    print("SVG and DXF views generated.")

    # PDF Report generation using rsvg-convert
    # Combine SVGs into a single PDF
    try:
        cmd = ["rsvg-convert", "-f", "pdf", "-o", "output/benchy_report.pdf"] + svg_files
        subprocess.run(cmd, check=True)
        print("PDF report generated using rsvg-convert.")
    except Exception as e:
        print(f"Failed to generate PDF: {e}")
        # Fallback to HTML
        html_content = f"""
<html>
<head><title>3DBenchy Report</title></head>
<body>
    <h1>3DBenchy Engineering Report</h1>
    <h2>Top View</h2>
    <img src="benchy_top.svg" width="400">
    <h2>Front View</h2>
    <img src="benchy_front.svg" width="400">
    <h2>Side View</h2>
    <img src="benchy_side.svg" width="400">
</body>
</html>
"""
        with open("output/benchy_report.html", "w") as f:
            f.write(html_content)
        print("HTML report generated as fallback.")

if __name__ == "__main__":
    generate_reports()
