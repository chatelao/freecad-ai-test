import sys
import os
from freecad_utils import setup_freecad_path

# Setup FreeCAD path
setup_freecad_path()
import FreeCAD
import TechDraw

def generate_reports():
    doc_path = "output/benchy.FCStd"
    if not os.path.exists(doc_path):
        print(f"Error: FreeCAD file not found at {doc_path}")
        return

    doc = FreeCAD.openDocument(doc_path)
    benchy_obj = doc.getObject("Benchy")
    shape = benchy_obj.Shape

    views = {
        "top": (0, 0, 1),
        "front": (0, -1, 0),
        "side": (1, 0, 0)
    }

    for name, direction in views.items():
        svg_file = f"output/benchy_{name}.svg"
        dxf_file = f"output/benchy_{name}.dxf"

        # TechDraw.projectToSVG(shape, dir_vec)
        # Note: direction must be a vector
        svg_content = TechDraw.projectToSVG(shape, FreeCAD.Vector(direction))
        with open(svg_file, "w") as f:
            f.write(svg_content)

        # TechDraw.projectToDXF(shape, dir_vec)
        dxf_content = TechDraw.projectToDXF(shape, FreeCAD.Vector(direction))
        with open(dxf_file, "w") as f:
            f.write(dxf_content)

        print(f"Generated {svg_file} and {dxf_file}")

    print("Reports (SVG and DXF) generated in output/ folder.")

if __name__ == "__main__":
    generate_reports()
