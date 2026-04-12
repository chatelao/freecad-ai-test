import sys
import os

# FreeCAD path discovery
# Search for common FreeCAD library paths or use environment variable
FREECAD_PATHS = [
    os.environ.get("FREECADPATH"),
    "/usr/lib/freecad-python3/lib",
    "/usr/lib/freecad/lib",
    "/usr/local/lib/freecad/lib"
]

for path in FREECAD_PATHS:
    if path and os.path.exists(path):
        if path not in sys.path:
            sys.path.append(path)
        break

try:
    import FreeCAD
    import Part
    import Mesh
except ImportError as e:
    print(f"Warning: Could not import FreeCAD modules. Ensure FreeCAD is installed and the library path is correct. Error: {e}")

def export_stl(objects, filename):
    """Export objects to STL file."""
    import Mesh
    Mesh.export(objects, filename)

def project_to_svg(shape, direction, output_file):
    """Project shape to SVG in the given direction."""
    import TechDraw
    # projectToSVG returns SVG content as string in FreeCAD 0.21
    svg_content = TechDraw.projectToSVG(shape, direction)
    if not svg_content.startswith("<?xml"):
        svg_header = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
        # Basic SVG tag wrapper if missing
        if not svg_content.strip().startswith("<svg"):
             if "<svg" not in svg_content:
                 svg_content = f'<svg xmlns="http://www.w3.org/2000/svg" version="1.1">\n{svg_content}\n</svg>'
        svg_content = svg_header + svg_content

    with open(output_file, 'w') as f:
        f.write(svg_content)

def project_to_dxf(shape, direction, output_file):
    """Project shape to DXF in the given direction."""
    import TechDraw
    dxf_content = TechDraw.projectToDXF(shape, direction)
    with open(output_file, 'w') as f:
        f.write(dxf_content)

def get_std_directions():
    """Returns standard view directions: Top, Front, Side (Right)."""
    import FreeCAD
    return {
        "top": FreeCAD.Vector(0, 0, 1),
        "front": FreeCAD.Vector(0, -1, 0),
        "side": FreeCAD.Vector(1, 0, 0)
    }
