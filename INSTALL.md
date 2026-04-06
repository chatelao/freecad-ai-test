# Installation Guide for FreeCAD Scripting and AI on Ubuntu

This guide covers the installation of FreeCAD and necessary Python packages to create and manipulate FreeCAD designs using scripting and AI.

## 1. Install FreeCAD and System Dependencies

To get the latest stable version of FreeCAD, it is recommended to use the official PPA.

```bash
sudo add-apt-repository ppa:freecad-maintainers/freecad-stable
sudo apt update
sudo apt install freecad python3-pivy python3-pyside2.qtcore python3-pyside2.qtgui python3-pyside2.qtwidgets python3-numpy
```

## 2. Install AI and Python Dependencies

Modern Ubuntu versions (23.04+) require the use of a virtual environment for Python packages to avoid conflicts with system-managed packages.

### Create and Activate a Virtual Environment

To use system-installed packages like `python3-pivy` and `python3-pyside2` within your virtual environment, use the `--system-site-packages` flag.

```bash
sudo apt install python3-venv
python3 -m venv --system-site-packages freecad_ai_env
source freecad_ai_env/bin/activate
```

### Install AI SDKs and Libraries

With the virtual environment activated, install the AI SDK of your choice and other necessary Python libraries.

```bash
pip install google-generativeai openai anthropic
```

For more advanced CAD operations, you might also want to install libraries like `scipy` or `pandas`.

## 3. Set up the Python Environment to Import FreeCAD

To use FreeCAD as a Python module in your own scripts, you must ensure that your Python interpreter can find it. The FreeCAD library is typically a file called `FreeCAD.so` on Linux.

### Find the FreeCAD Library Path

Run the following command to find where `FreeCAD.so` is installed:

```bash
find /usr/lib -name FreeCAD.so
```

### Import FreeCAD in Your Python Script

Once you have discovered the path (e.g., `/usr/lib/freecad/lib`), you can use the following code snippet at the beginning of your Python script:

```python
import sys
# Replace with the actual path discovered on your system
FREECADPATH = '/usr/lib/freecad/lib'
sys.path.append(FREECADPATH)

try:
    import FreeCAD
except ImportError:
    print("Error: Could not find FreeCAD library. Please check FREECADPATH.")
```
