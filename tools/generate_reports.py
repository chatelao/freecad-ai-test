import os
import sys
import random
import subprocess

# Add the root directory to sys.path to find freecad_utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import freecad_utils

def export_view(FreeCAD, Part, TechDraw, shape, direction, filename):
    print(f"Exporting view to {filename}...")
    # TechDraw.projectToSVG returns SVG string in FreeCAD 0.21
    svg_content = TechDraw.projectToSVG(shape, direction)

    # Prepend XML declaration and wrap if necessary (based on memory)
    if not svg_content.startswith("<?xml"):
        full_svg = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
        full_svg += '<svg xmlns="http://www.w3.org/2000/svg" version="1.1">\n'
        full_svg += svg_content
        full_svg += '\n</svg>'
    else:
        full_svg = svg_content

    with open(filename, "w") as f:
        f.write(full_svg)

def generate_reports():
    FreeCAD = freecad_utils.init_freecad()
    import Part
    import TechDraw

    doc = FreeCAD.open("output/benchy.FCStd")
    obj = doc.getObject("Benchy")
    shape = obj.Shape

    # Standard Views
    views = {
        "top": FreeCAD.Vector(0, 0, 1),
        "front": FreeCAD.Vector(0, -1, 0),
        "side": FreeCAD.Vector(1, 0, 0)
    }

    svg_files = []
    for name, direction in views.items():
        filename = f"output/benchy_{name}.svg"
        export_view(FreeCAD, Part, TechDraw, shape, direction, filename)
        svg_files.append(filename)

    # 6 Random Views
    for i in range(6):
        direction = FreeCAD.Vector(
            random.uniform(-1, 1),
            random.uniform(-1, 1),
            random.uniform(-1, 1)
        ).normalize()
        filename = f"output/benchy_random_{i}.svg"
        export_view(FreeCAD, Part, TechDraw, shape, direction, filename)
        svg_files.append(filename)

    # Combine to PDF using rsvg-convert (if available)
    print("Generating PDF report...")
    pdf_output = "output/benchy_report.pdf"
    try:
        # Sort files to have standard views first
        cmd = ["rsvg-convert", "-f", "pdf", "-o", pdf_output] + svg_files
        subprocess.run(cmd, check=True)
        print(f"Report generated: {pdf_output}")
    except Exception as e:
        print(f"Failed to generate PDF: {e}")

if __name__ == "__main__":
    generate_reports()
