import sys
import os

def setup_freecad():
    # Common paths for FreeCAD Python library
    candidate_paths = [
        "/usr/lib/freecad-python3/lib",
        "/usr/lib/freecad/lib",
        "/usr/local/lib/freecad/lib",
    ]

    # Check if FREECADPATH is set in environment
    env_path = os.environ.get("FREECADPATH")
    if env_path:
        candidate_paths.insert(0, env_path)

    for path in candidate_paths:
        if os.path.exists(os.path.join(path, "FreeCAD.so")):
            if path not in sys.path:
                sys.path.append(path)
            return True

    # Try finding via find command if candidates fail
    import subprocess
    try:
        result = subprocess.run(["find", "/usr/lib", "-name", "FreeCAD.so"], capture_output=True, text=True)
        if result.returncode == 0 and result.stdout:
            path = os.path.dirname(result.stdout.splitlines()[0])
            if path not in sys.path:
                sys.path.append(path)
            return True
    except:
        pass

    return False

def get_template_path():
    # Common paths for TechDraw templates
    candidate_paths = [
        "/usr/share/freecad/Mod/TechDraw/Templates/A4_Landscape_blank.svg",
        "/usr/lib/freecad/Mod/TechDraw/Templates/A4_Landscape_blank.svg",
    ]

    for path in candidate_paths:
        if os.path.exists(path):
            return path
    return None
