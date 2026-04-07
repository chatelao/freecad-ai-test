import sys
import os
from freecad_utils import setup_freecad

if not setup_freecad():
    print("FreeCAD library not found.")
    sys.exit(1)

import FreeCAD
import TechDraw

def generate_reports():
    doc = FreeCAD.open("output/benchy.FCStd")
    benchy = doc.getObject("Benchy")

    if benchy is None:
        print("Error: Benchy object not found.")
        sys.exit(1)

    # Use TechDraw to project views directly
    # projectToSVG(shape, direction, scale, rotation)
    # top: Z(0,0,1)
    # front: X(1,0,0)
    # side: Y(0,1,0)

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    top_svg = TechDraw.projectToSVG(benchy.Shape, FreeCAD.Vector(0,0,1))
    front_svg = TechDraw.projectToSVG(benchy.Shape, FreeCAD.Vector(1,0,0))
    side_svg = TechDraw.projectToSVG(benchy.Shape, FreeCAD.Vector(0,1,0))

    # Write a simple combined SVG
    with open(os.path.join(output_dir, "benchy_report.svg"), "w") as f:
        f.write('<svg width="800" height="600" xmlns="http://www.w3.org/2000/svg">\n')
        # We need to wrap each projected SVG properly or just dump them with offsets
        f.write('<g transform="translate(50, 50)">\n')
        f.write(top_svg)
        f.write('</g>\n')
        f.write('<g transform="translate(300, 50)">\n')
        f.write(front_svg)
        f.write('</g>\n')
        f.write('<g transform="translate(550, 50)">\n')
        f.write(side_svg)
        f.write('</g>\n')
        f.write('</svg>\n')

    # For DXF, use projectToDXF
    top_dxf = TechDraw.projectToDXF(benchy.Shape, FreeCAD.Vector(0,0,1))
    front_dxf = TechDraw.projectToDXF(benchy.Shape, FreeCAD.Vector(1,0,0))
    side_dxf = TechDraw.projectToDXF(benchy.Shape, FreeCAD.Vector(0,1,0))

    with open(os.path.join(output_dir, "benchy_report.dxf"), "w") as f:
        # DXF is harder to combine by hand, just write top for now or use multiple files
        f.write(top_dxf)

    print("Reports generated in output/ directory.")

if __name__ == "__main__":
    generate_reports()
