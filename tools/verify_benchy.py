import os
import sys
import xml.etree.ElementTree as ET

# Add the root directory to sys.path to find freecad_utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import freecad_utils

def verify_stl(filepath):
    FreeCAD = freecad_utils.init_freecad()
    import Mesh

    print(f"Verifying STL: {filepath}")
    # Mesh.read is preferred to prevent segfaults in headless environments
    mesh = Mesh.read(filepath)
    bbox = mesh.BoundBox

    L, W, H = bbox.XLength, bbox.YLength, bbox.ZLength
    print(f"Dimensions: {L:.2f} x {W:.2f} x {H:.2f}")

    target_l, target_w, target_h = 60.0, 31.0, 48.0
    accuracy_l = 100 * (1 - abs(L - target_l) / target_l)
    accuracy_w = 100 * (1 - abs(W - target_w) / target_w)
    accuracy_h = 100 * (1 - abs(H - target_h) / target_h)

    print(f"Accuracy: L:{accuracy_l:.2f}%, W:{accuracy_w:.2f}%, H:{accuracy_h:.2f}%")

    valid = accuracy_l >= 99.5 and accuracy_w >= 99.5 and accuracy_h >= 99.5
    return valid

def verify_svg_headers(directory):
    print(f"Verifying SVG headers in {directory}")
    all_valid = True
    for f in os.listdir(directory):
        if f.endswith(".svg"):
            path = os.path.join(directory, f)
            try:
                with open(path, 'r') as file:
                    content = file.read().strip()

                # Check for XML declaration and SVG tag
                has_xml_dec = content.startswith("<?xml")
                has_svg_tag = "<svg" in content and "xmlns" in content

                if not (has_xml_dec and has_svg_tag):
                    print(f"  [FAIL] {f}: Missing XML declaration or valid SVG tag")
                    all_valid = False
                else:
                    # Try parsing
                    ET.fromstring(content)
                    print(f"  [PASS] {f}")
            except Exception as e:
                print(f"  [ERROR] {f}: {e}")
                all_valid = False
    return all_valid

def main():
    stl_path = "benchy.stl"
    if not os.path.exists(stl_path):
        stl_path = "output/benchy.stl"

    if os.path.exists(stl_path):
        stl_valid = verify_stl(stl_path)
        print(f"STL Validation ({stl_path}): {'SUCCESS' if stl_valid else 'FAILURE'}")
    else:
        print(f"STL not found: {stl_path}")

    # Check SVG headers in output directory where they are generated
    svg_valid = verify_svg_headers("output")
    print(f"SVG Header Validation: {'SUCCESS' if svg_valid else 'FAILURE'}")

if __name__ == "__main__":
    main()
