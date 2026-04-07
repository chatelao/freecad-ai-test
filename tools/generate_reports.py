import sys
import os
import random

# Add the path to FreeCAD
from freecad_utils import setup_freecad, get_techdraw_template
if not setup_freecad():
    print("FreeCAD not found")
    sys.exit(1)

import FreeCAD
import Part
import TechDraw

def generate_reports():
    fcstd_path = "output/benchy.FCStd"
    if not os.path.exists(fcstd_path):
        print("FCStd file not found")
        return

    doc = FreeCAD.open(fcstd_path)
    obj = doc.getObject("Benchy")

    # 6 Random Views
    for i in range(6):
        rand_dir = FreeCAD.Vector(random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        svg_path = f"output/view_random_{i+1}.svg"
        try:
            svg_content = TechDraw.projectToSVG(obj.Shape, rand_dir)
            with open(svg_path, "w") as f:
                f.write(svg_content)
            print(f"Exported {svg_path}")
        except Exception as e:
            print(f"Failed to export {svg_path}: {e}")

    # Standard Views
    views = [
        ('Front', FreeCAD.Vector(0, -1, 0)),
        ('Top', FreeCAD.Vector(0, 0, 1)),
        ('Side', FreeCAD.Vector(1, 0, 0))
    ]

    for name, direction in views:
        svg_path = f"output/view_{name.lower()}.svg"
        try:
            svg_content = TechDraw.projectToSVG(obj.Shape, direction)
            with open(svg_path, "w") as f:
                f.write(svg_content)
            print(f"Exported {svg_path}")
        except Exception as e:
            print(f"Failed to export {svg_path}: {e}")

    # TechDraw Setup for PDF (Only if template exists)
    template_path = get_techdraw_template()
    if template_path:
        try:
            page = doc.addObject('TechDraw::DrawPage', 'Page')
            template = doc.addObject('TechDraw::DrawSVGTemplate', 'Template')
            template.Template = template_path
            page.Template = template

            # Standard views in TechDraw Page
            view_front = doc.addObject('TechDraw::DrawViewPart', 'FrontView')
            view_front.Source = [obj]
            view_front.Direction = FreeCAD.Vector(0, -1, 0)
            view_front.X = 100
            view_front.Y = 100
            page.addView(view_front)

            view_top = doc.addObject('TechDraw::DrawViewPart', 'TopView')
            view_top.Source = [obj]
            view_top.Direction = FreeCAD.Vector(0, 0, 1)
            view_top.X = 100
            view_top.Y = 180
            page.addView(view_top)

            view_side = doc.addObject('TechDraw::DrawViewPart', 'SideView')
            view_side.Source = [obj]
            view_side.Direction = FreeCAD.Vector(1, 0, 0)
            view_side.X = 180
            view_side.Y = 100
            page.addView(view_side)

            doc.recompute()
            pdf_path = "output/benchy_report.pdf"
            page.exportPDF(pdf_path)
            print(f"Report exported to {pdf_path}")
        except Exception as e:
            print(f"Failed to generate PDF report: {e}")
    else:
        print("Skipping PDF generation as no template was found.")

    doc.save()
    FreeCAD.closeDocument(doc.Name)

if __name__ == "__main__":
    generate_reports()
