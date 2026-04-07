import sys
import os

def setup_freecad_path():
    # Common paths for FreeCAD on Ubuntu
    possible_paths = [
        '/usr/lib/freecad-python3/lib',
        '/usr/lib/freecad/lib',
        '/usr/local/lib/freecad/lib',
    ]

    # Check if FREECADPATH is set in environment
    env_path = os.environ.get('FREECADPATH')
    if env_path:
        possible_paths.insert(0, env_path)

    for path in possible_paths:
        if os.path.exists(os.path.join(path, 'FreeCAD.so')) or os.path.exists(os.path.join(path, 'FreeCAD.pyd')):
            sys.path.append(path)
            return True

    return False

def get_techdraw_template_path():
    # Standard location for TechDraw templates
    template_path = '/usr/share/freecad/Mod/TechDraw/Templates/A4_LandscapeTD.svg'
    if os.path.exists(template_path):
        return template_path
    return None
