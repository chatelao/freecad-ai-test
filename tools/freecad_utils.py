import sys
import os

# FreeCAD path discovery
FREECADPATH = os.environ.get('FREECADPATH', '/usr/lib/freecad-python3/lib')

def setup_freecad():
    # Common installation paths
    alternatives = [
        FREECADPATH,
        '/usr/lib/freecad/lib',
        '/usr/local/lib/freecad/lib',
        '/usr/lib/freecad-python3/lib'
    ]

    found_path = None
    for alt in alternatives:
        if os.path.exists(alt):
            if alt not in sys.path:
                sys.path.append(alt)
            found_path = alt
            break

    try:
        import FreeCAD
        import Part
        import Mesh
        import TechDraw
        try:
            import PartDesign
        except ImportError:
            import _PartDesign as PartDesign

        print(f"FreeCAD {FreeCAD.Version()[0]}.{FreeCAD.Version()[1]} found at {found_path}")
        return FreeCAD, Part, PartDesign, Mesh, TechDraw
    except ImportError as e:
        print(f"Error: Could not find FreeCAD library. {e}")
        print(f"Search paths: {sys.path}")
        sys.exit(1)

def get_techdraw_template():
    # Standard locations for TechDraw templates
    possible_locations = [
        "/usr/share/freecad/Mod/TechDraw/Templates/A4_Landscape_blank.svg",
        "/usr/lib/freecad-python3/Mod/TechDraw/Templates/A4_Landscape_blank.svg",
        "/usr/lib/freecad/Mod/TechDraw/Templates/A4_Landscape_blank.svg"
    ]
    for loc in possible_locations:
        if os.path.exists(loc):
            return loc
    return None
