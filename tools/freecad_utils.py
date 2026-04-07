import sys
import os

def get_freecad_path():
    paths = [
        '/usr/lib/freecad-python3/lib',
        '/usr/lib/freecad/lib',
        '/usr/local/lib/freecad/lib'
    ]
    env_path = os.environ.get('FREECADPATH')
    if env_path:
        paths.insert(0, env_path)

    for path in paths:
        if os.path.exists(os.path.join(path, 'FreeCAD.so')):
            return path
    return None

def setup_freecad():
    path = get_freecad_path()
    if path:
        sys.path.append(path)
        return True
    return False
