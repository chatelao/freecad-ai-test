import sys
import os
import subprocess

def setup_freecad_paths():
    """Finds and adds FreeCAD library paths to sys.path."""
    # Priority paths from memory and common locations
    potential_paths = [
        "/usr/lib/freecad-python3/lib",
        "/usr/lib/freecad/lib",
        "/usr/local/lib/freecad/lib",
        "/usr/lib/freecad-python3/lib/FreeCAD.so", # check if it's the directory we need
    ]

    # Check FREECADPATH environment variable
    env_path = os.environ.get("FREECADPATH")
    if env_path:
        potential_paths.insert(0, env_path)

    # Standard locations to search
    search_roots = ["/usr/lib", "/usr/local/lib"]

    found_paths = []
    for path in potential_paths:
        if os.path.exists(path):
            if os.path.isfile(path):
                path = os.path.dirname(path)
            if path not in found_paths:
                found_paths.append(path)

    if not found_paths:
        # Fallback to searching with find
        for root in search_roots:
            try:
                result = subprocess.run(
                    ["find", root, "-name", "FreeCAD.so"],
                    capture_output=True, text=True, timeout=10
                )
                if result.stdout:
                    for line in result.stdout.splitlines():
                        d = os.path.dirname(line)
                        if d not in found_paths:
                            found_paths.append(d)
            except Exception:
                pass

    for path in found_paths:
        if path not in sys.path:
            sys.path.append(path)

    # Add OpenSCAD module path for exportCSG
    openscad_mod_path = "/usr/share/freecad/Mod/OpenSCAD/"
    if os.path.exists(openscad_mod_path) and openscad_mod_path not in sys.path:
        sys.path.append(openscad_mod_path)

def get_template_path():
    """Returns path to a standard TechDraw template."""
    paths = [
        "/usr/share/freecad/Mod/TechDraw/Templates/A4_Landscape_blank.svg",
        "/usr/share/freecad/Mod/TechDraw/Templates/A3_Landscape_blank.svg"
    ]
    for p in paths:
        if os.path.exists(p):
            return p
    return None

def init_freecad():
    """Initializes FreeCAD environment and returns the FreeCAD module."""
    setup_freecad_paths()
    import FreeCAD
    return FreeCAD

def get_python_exe():
    """Returns a python executable compatible with FreeCAD."""
    exes = [
        "/usr/bin/freecad-python3",
        "/usr/bin/freecadcmd-python3",
        sys.executable
    ]
    for exe in exes:
        if os.path.exists(exe):
            return exe
    return "python3"
