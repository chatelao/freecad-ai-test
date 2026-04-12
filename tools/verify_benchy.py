import sys
import os
import glob

# Add tools dir to sys.path
sys.path.append(os.path.dirname(__file__))
import freecad_utils
import Mesh

def verify_stl(filepath):
    print(f"Verifying STL: {filepath}")
    # Using Mesh.read instead of Mesh.Mesh to avoid segfaults in headless
    mesh = Mesh.read(filepath)
    bbox = mesh.BoundBox

    # Expected: 60 x 31 x 48
    print(f"Bounding Box: L={bbox.XLength:.2f}, W={bbox.YLength:.2f}, H={bbox.ZLength:.2f}")

    l_acc = abs(bbox.XLength - 60.0) / 60.0
    w_acc = abs(bbox.YLength - 31.0) / 31.0
    h_acc = abs(bbox.ZLength - 48.0) / 48.0

    print(f"Accuracy: L={100*(1-l_acc):.2f}%, W={100*(1-w_acc):.2f}%, H={100*(1-h_acc):.2f}%")

    if l_acc < 0.005 and w_acc < 0.005 and h_acc < 0.005:
        print("STL Accuracy Check: PASSED")
        return True
    else:
        print("STL Accuracy Check: FAILED")
        return False

def verify_svg(filepath):
    print(f"Verifying SVG: {filepath}")
    with open(filepath, 'r') as f:
        content = f.read().strip()

    has_xml = content.startswith("<?xml")
    has_svg = "<svg" in content

    if has_xml and has_svg:
        print(f"SVG Header Check: PASSED")
        return True
    else:
        print(f"SVG Header Check: FAILED (xml={has_xml}, svg={has_svg})")
        return False

def main():
    results = []

    # Check STL in root or output
    stl_files = glob.glob("benchy.stl") + glob.glob("output/benchy.stl")
    if stl_files:
        results.append(verify_stl(stl_files[0]))
    else:
        print("No STL file found to verify.")
        results.append(False)

    # Check SVGs in output
    svg_files = glob.glob("output/*.svg")
    if svg_files:
        for svg in svg_files:
            results.append(verify_svg(svg))
    else:
        print("No SVG files found in output/ to verify.")

    if all(results) and results:
        print("\nOVERALL VALIDATION: PASSED")
        sys.exit(0)
    else:
        print("\nOVERALL VALIDATION: FAILED")
        sys.exit(1)

if __name__ == "__main__":
    main()
