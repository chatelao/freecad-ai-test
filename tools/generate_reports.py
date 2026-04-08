import sys
import os
import random

# Import utility
from freecad_utils import setup_freecad

if not setup_freecad():
    print("FreeCAD not found. Exiting.")
    sys.exit(1)

import FreeCAD
import Part
import TechDraw

def generate_reports():
    if not os.path.exists("benchy.FCStd"):
        print("benchy.FCStd not found.")
        return

    doc = FreeCAD.open("benchy.FCStd")
    obj = doc.getObject("Benchy")

    # Create output directory
    os.makedirs("output/views", exist_ok=True)

    # Standard views
    views = {
        "top": (0, 0, 1),
        "front": (0, -1, 0),
        "side": (1, 0, 0)
    }

    for name, direction in views.items():
        svg = TechDraw.projectToSVG(obj.Shape, FreeCAD.Base.Vector(*direction))
        with open(f"output/views/{name}.svg", "w") as f:
            f.write(svg)

    # 6 Random views
    for i in range(6):
        direction = [random.uniform(-1, 1) for _ in range(3)]
        vec = FreeCAD.Base.Vector(*direction)
        vec.normalize()
        svg = TechDraw.projectToSVG(obj.Shape, vec)
        with open(f"output/views/random_{i}.svg", "w") as f:
            f.write(svg)

    print("SVG views generated.")

    # Try to export as PDF via TechDraw Page
    page = doc.addObject('TechDraw::DrawPage', 'Page')
    template = doc.addObject('TechDraw::DrawSVGTemplate', 'Template')
    template.Template = '/usr/share/freecad/Mod/TechDraw/Templates/A4_Landscape_blank.svg'
    page.Template = template

    # Add views to page
    for i, (name, direction) in enumerate(views.items()):
        view = doc.addObject('TechDraw::DrawViewPart', f'View_{name}')
        view.Source = [obj]
        view.Direction = FreeCAD.Base.Vector(*direction)
        page.addView(view)
        view.X = 50 + i * 80
        view.Y = 100
        view.Scale = 2.0

    doc.recompute()

    # In some versions it's page.exportPdf() or similar.
    # Since exportPageAsPdf failed, let's try a more robust approach.
    exported = False
    try:
        # Check if Page has an export method
        if hasattr(page, 'exportPdf'):
             page.exportPdf("output/report.pdf")
             exported = True
    except:
        pass

    if not exported:
        # We'll use the HTML report as the primary report since PDF is flaky in this headless env
        html_report()
    else:
        print("PDF Report generated at output/report.pdf")

def html_report():
    html_content = """
    <html>
    <head>
        <style>
            body { font-family: sans-serif; margin: 20px; }
            img { border: 1px solid #ccc; margin: 10px; }
        </style>
    </head>
    <body>
        <h1>3DBenchy Report</h1>
        <h2>Standard Views</h2>
        <div>
            <figure style="display:inline-block">
                <img src="views/top.svg" width="300">
                <figcaption>Top View</figcaption>
            </figure>
            <figure style="display:inline-block">
                <img src="views/front.svg" width="300">
                <figcaption>Front View</figcaption>
            </figure>
            <figure style="display:inline-block">
                <img src="views/side.svg" width="300">
                <figcaption>Side View</figcaption>
            </figure>
        </div>
        <h2>Random Perspective Views</h2>
        <div>
    """
    for i in range(6):
        html_content += f'<img src="views/random_{i}.svg" width="200">'

    html_content += """
        </div>
    </body>
    </html>
    """
    with open("output/report.html", "w") as f:
        f.write(html_content)
    print("HTML Report generated at output/report.html")

if __name__ == "__main__":
    generate_reports()
