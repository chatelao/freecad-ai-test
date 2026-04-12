import sys
import os

def setup_freecad():
    """Finds and adds FreeCAD libraries to sys.path."""
    paths = [
        "/usr/lib/freecad-python3/lib",
        "/usr/lib/freecad/lib",
        "/usr/local/lib/freecad/lib"
    ]

    env_path = os.environ.get("FREECADPATH")
    if env_path:
        paths.insert(0, env_path)

    found = False
    for path in paths:
        if os.path.exists(os.path.join(path, "FreeCAD.so")):
            sys.path.append(path)
            found = True
            break

    if not found:
        # Fallback to search
        import subprocess
        try:
            result = subprocess.run(["find", "/usr/lib", "-name", "FreeCAD.so"], capture_output=True, text=True)
            if result.stdout:
                path = os.path.dirname(result.stdout.splitlines()[0])
                sys.path.append(path)
                found = True
        except Exception:
            pass

    if not found:
        raise ImportError("Could not find FreeCAD.so in standard paths.")

    import FreeCAD
    import Part
    import Mesh
    try:
        import _PartDesign as PartDesign
    except ImportError:
        import PartDesign

    return FreeCAD, Part, Mesh, PartDesign

def get_template_path():
    """Returns the path to a TechDraw template."""
    standard_paths = [
        "/usr/share/freecad/Mod/TechDraw/Templates/A4_Landscape_blank.svg",
        "/usr/share/freecad/Mod/TechDraw/Templates/A4_Landscape_TD.svg"
    ]
    for p in standard_paths:
        if os.path.exists(p):
            return p
    return None
