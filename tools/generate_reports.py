import sys
import os
from freecad_utils import setup_freecad

FreeCAD, Part, Mesh, PartDesign = setup_freecad()
import TechDraw

def export_views():
    doc = FreeCAD.open("benchy.fcstd")
    benchy = doc.getObject("Benchy")
    shape = benchy.Shape

    views = {
        "top": FreeCAD.Vector(0, 0, 1),
        "front": FreeCAD.Vector(0, -1, 0),
        "side": FreeCAD.Vector(1, 0, 0)
    }

    os.makedirs("output", exist_ok=True)

    for name, direction in views.items():
        # SVG
        svg_content = TechDraw.projectToSVG(shape, direction)
        # Wrap in minimal SVG tag if needed, but projectToSVG usually returns a fragment or full depending on version
        # In 0.21, it returns a string with <svg> tag.

        # Ensure XML declaration and namespace
        if not svg_content.startswith("<?xml"):
            header = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
            # If it doesn't start with <svg, wrap it
            if not svg_content.strip().startswith("<svg"):
                # Wrap with a basic SVG tag
                svg_content = header + '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="200mm" height="200mm" viewBox="-100 -100 200 200">\n' + svg_content + '\n</svg>'
            else:
                svg_content = header + svg_content

        # TechDraw.projectToSVG might not include the namespace in the <svg> tag if it's just a fragment
        if 'xmlns="http://www.w3.org/2000/svg"' not in svg_content:
             svg_content = svg_content.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1)

        svg_path = f"output/benchy_{name}.svg"
        with open(svg_path, "w") as f:
            f.write(svg_content)
        print(f"Exported {svg_path}")

        # DXF
        dxf_content = TechDraw.projectToDXF(shape, direction)
        dxf_path = f"output/benchy_{name}.dxf"
        with open(dxf_path, "w") as f:
            f.write(dxf_content)
        print(f"Exported {dxf_path}")

if __name__ == "__main__":
    export_views()
