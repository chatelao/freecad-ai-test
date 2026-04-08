import sys
import os

def setup_freecad():
    """Adds FreeCAD library paths to sys.path dynamically."""
    potential_paths = [
        os.environ.get("FREECADPATH"),
        "/usr/lib/freecad-python3/lib",
        "/usr/lib/freecad/lib",
        "/usr/local/lib/freecad/lib",
    ]

    # Also check for FreeCAD.so using find-like logic if possible,
    # but here we'll stick to common locations for stability.

    found = False
    for path in potential_paths:
        if path and os.path.exists(path):
            if path not in sys.path:
                sys.path.append(path)
            found = True
            print(f"Using FreeCAD path: {path}")
            break

    try:
        import FreeCAD
        print(f"FreeCAD {FreeCAD.Version()} successfully imported")
        return True
    except ImportError as e:
        print(f"Failed to import FreeCAD: {e}")
        return False

def export_stl(doc, filename):
    """Exports the entire document to an STL file."""
    import Mesh
    # Select all visible objects
    objs = [o for o in doc.Objects if hasattr(o, "Shape")]
    Mesh.export(objs, filename)
    print(f"Exported to {filename}")

def export_svg(shape, filename, direction=(0, 0, 1)):
    """Exports a shape to an SVG file."""
    import FreeCAD
    import TechDraw
    try:
        dir_vec = FreeCAD.Vector(direction[0], direction[1], direction[2])
        # In FreeCAD 0.21+, projectToSVG might return a string
        svg_content = TechDraw.projectToSVG(shape, dir_vec)
        with open(filename, 'w') as f:
            f.write(svg_content)
        print(f"Exported to {filename}")
    except Exception as e:
        print(f"Failed to export SVG to {filename}: {e}")

if __name__ == "__main__":
    setup_freecad()
