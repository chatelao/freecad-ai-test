import sys
import os

def setup_freecad():
    # Common locations for FreeCAD on Linux systems
    potential_paths = [
        "/usr/lib/freecad-python3/lib",
        "/usr/lib/freecad/lib",
        "/usr/local/lib/freecad/lib",
    ]

    # Also check FREECADPATH environment variable
    env_path = os.environ.get("FREECADPATH")
    if env_path:
        potential_paths.insert(0, env_path)

    for path in potential_paths:
        if os.path.exists(path):
            if path not in sys.path:
                sys.path.append(path)
            return True

    return False

def get_template_path(template_name="A3_LandscapeTD.svg"):
    standard_path = f"/usr/share/freecad/Mod/TechDraw/Templates/{template_name}"
    if os.path.exists(standard_path):
        return standard_path
    return None
