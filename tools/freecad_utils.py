import os
import sys

def setup_freecad():
    # Common FreeCAD paths
    potential_paths = [
        "/usr/lib/freecad-python3/lib",
        "/usr/lib/freecad/lib",
        "/usr/local/lib/freecad/lib",
    ]

    if "FREECADPATH" in os.environ:
        potential_paths.insert(0, os.environ["FREECADPATH"])

    for path in potential_paths:
        if os.path.exists(path):
            if path not in sys.path:
                sys.path.append(path)
            break
    else:
        print("Warning: FreeCAD path not found automatically.")

    try:
        import FreeCAD
        return True
    except ImportError:
        return False

def wrap_svg(svg_content):
    if not svg_content.startswith('<?xml'):
        header = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
        if '<svg' not in svg_content:
             # Basic wrapper if it's just paths
             svg_content = f'<svg xmlns="http://www.w3.org/2000/svg" version="1.1">\n{svg_content}\n</svg>'
        else:
             svg_content = header + svg_content
    return svg_content

def get_techdraw_templates():
    standard_path = "/usr/share/freecad/Mod/TechDraw/Templates/"
    if os.path.exists(standard_path):
        return [os.path.join(standard_path, f) for f in os.listdir(standard_path) if f.endswith(".svg")]
    return []
