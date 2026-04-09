import sys
import os
import subprocess

def setup_freecad():
    """Finds and adds FreeCAD library paths to sys.path."""
    fc_paths = [
        "/usr/lib/freecad-python3/lib",
        "/usr/lib/freecad/lib",
        "/usr/local/lib/freecad/lib"
    ]

    # Try to find path using find command if defaults fail
    if not any(os.path.exists(p) for p in fc_paths):
        try:
            result = subprocess.run(["find", "/usr/lib", "-name", "FreeCAD.so"], capture_output=True, text=True)
            if result.stdout:
                found_path = os.path.dirname(result.stdout.splitlines()[0])
                fc_paths.insert(0, found_path)
        except Exception:
            pass

    if "FREECADPATH" in os.environ:
        fc_paths.insert(0, os.environ["FREECADPATH"])

    found = False
    for path in fc_paths:
        if os.path.exists(path):
            if path not in sys.path:
                sys.path.append(path)
            found = True
            break

    if not found:
        print("Warning: FreeCAD library path not found. Ensure FreeCAD is installed.")

    try:
        import FreeCAD
        import Part
        import Mesh
        return True
    except ImportError as e:
        print(f"Error: Could not import FreeCAD modules: {e}")
        return False

def get_template_path(template_name="A4_Landscape_Blank.svg"):
    """Returns the path to a TechDraw template."""
    common_paths = [
        "/usr/share/freecad/Mod/TechDraw/Templates/",
        "/usr/lib/freecad/Mod/TechDraw/Templates/"
    ]
    for path in common_paths:
        full_path = os.path.join(path, template_name)
        if os.path.exists(full_path):
            return full_path
    return None

def ensure_output_dir(directory="output"):
    """Ensures the output directory exists."""
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory
