import sys
import os
import random
import re

# Add the path to FreeCAD
from freecad_utils import setup_freecad, get_techdraw_template
if not setup_freecad():
    print("FreeCAD not found")
    sys.exit(1)

import FreeCAD
import Part
import TechDraw

def save_valid_svg(svg_content, filepath):
    """Wraps SVG fragment in a valid <svg> root element."""
    # Find coordinates only within path data 'd="..."'
    # Pattern: d=" ... "
    all_d = re.findall(r'd\s*=\s*"([^"]+)"', svg_content)
    coords_str = " ".join(all_d)
    # Extract numbers from path data
    coords = re.findall(r'([-+]?\d*\.\d+|[-+]?\d+)', coords_str)

    if coords:
        floats = [float(c) for c in coords]
        # We assume they are x,y pairs.
        # However, path data can have single values (e.g. for H or V commands)
        # To be safe, let's just find min/max of all numbers and use them for both X and Y bounds
        min_val = min(floats)
        max_val = max(floats)

        width = max_val - min_val
        height = width # Keep it square if we're not sure

        # A better approach if we assume x,y:
        # But wait, svg_content might have transform="scale(1, -1)" which flips Y.
        # Let's just use a large enough viewBox or try to parse better.

        xs = floats[::2]
        ys = floats[1::2]
        if xs and ys:
            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)
            viewbox = f"{min_x-5} {min_y-5} {max_x-min_x+10} {max_y-min_y+10}"
        else:
            viewbox = f"{min_val-5} {min_val-5} {width+10} {width+10}"
    else:
        viewbox = "-100 -100 200 200"

    full_svg = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" version="1.1" viewBox="{viewbox}">
{svg_content}
</svg>"""
    with open(filepath, "w") as f:
        f.write(full_svg)

def generate_reports():
    fcstd_path = "output/benchy.FCStd"
    if not os.path.exists(fcstd_path):
        fcstd_path = "benchy.FCStd"
        if not os.path.exists(fcstd_path):
            print("FCStd file not found")
            return

    doc = FreeCAD.open(fcstd_path)
    obj = doc.getObject("Benchy")
    if not obj:
        print("Benchy object not found")
        return

    # Random Views (6)
    for i in range(6):
        rand_dir = FreeCAD.Vector(random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        svg_path = f"output/view_random_{i+1}.svg"
        try:
            svg_content = TechDraw.projectToSVG(obj.Shape, rand_dir)
            save_valid_svg(svg_content, svg_path)
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
            save_valid_svg(svg_content, svg_path)
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

            view_front = doc.addObject('TechDraw::DrawViewPart', 'FrontView')
            view_front.Source = [obj]
            view_front.Direction = FreeCAD.Vector(0, -1, 0)
            view_front.X = 100
            view_front.Y = 100
            page.addView(view_front)

            doc.recompute()
            pdf_path = "output/benchy_report.pdf"
            page.exportPDF(pdf_path)
            print(f"Report exported to {pdf_path}")
        except Exception as e:
            print(f"Failed to generate PDF report: {e}")

    doc.save()
    FreeCAD.closeDocument(doc.Name)

if __name__ == "__main__":
    generate_reports()
