import sys
import os

def setup_freecad():
    """
    Search for FreeCAD and append to sys.path
    """
    FREECAD_PATHS = [
        '/usr/lib/freecad-python3/lib',
        '/usr/lib/freecad/lib',
        '/usr/local/lib/freecad/lib'
    ]

    # Check if FREECADPATH environment variable is set
    env_path = os.environ.get('FREECADPATH')
    if env_path:
        FREECAD_PATHS.insert(0, env_path)

    found = False
    for path in FREECAD_PATHS:
        if os.path.exists(os.path.join(path, 'FreeCAD.so')):
            sys.path.append(path)
            found = True
            break

    if not found:
        # Try finding it if not in standard locations
        import subprocess
        try:
            res = subprocess.check_output(['find', '/usr/lib', '-name', 'FreeCAD.so'], stderr=subprocess.STDOUT)
            if res:
                path = os.path.dirname(res.decode().strip().split('\n')[0])
                sys.path.append(path)
                found = True
        except:
            pass

    if not found:
        print("Warning: FreeCAD library not found. Scripts may fail.")
    else:
        try:
            import FreeCAD
            import Part
            import Mesh
            return True
        except ImportError as e:
            print(f"Error importing FreeCAD: {e}")
            return False

def get_techdraw_template():
    """
    Return path to a standard TechDraw template
    """
    possible_templates = [
        '/usr/share/freecad/Mod/TechDraw/Templates/A4_Landscape_ISO7200TD.svg',
        '/usr/share/freecad/Mod/TechDraw/Templates/A4_Portrait_ISO7200TD.svg'
    ]
    for t in possible_templates:
        if os.path.exists(t):
            return t
    return None

if __name__ == "__main__":
    if setup_freecad():
        import FreeCAD
        print(f"FreeCAD {FreeCAD.Version()} found and initialized.")
    else:
        print("Failed to initialize FreeCAD.")
