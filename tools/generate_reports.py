import os
import sys

from freecad_utils import setup_freecad, get_techdraw_template

FreeCAD, Part, PartDesign, Mesh, TechDraw = setup_freecad()

def generate_reports(doc_path):
    print(f"Opening {doc_path} for report generation...")
    doc = FreeCAD.openDocument(doc_path)

    # Locate the fusion object
    objs = doc.findObjects(Name="BenchyBody")
    if not objs:
        print("Error: Could not find 'BenchyBody' object.")
        return
    body = objs[0]

    # Views: Front, Top, Side (Right)
    views = [
        ("Front", FreeCAD.Vector(1, 0, 0)),
        ("Top", FreeCAD.Vector(0, 0, 1)),
        ("Side", FreeCAD.Vector(0, 1, 0))
    ]

    output_dir = os.path.dirname(doc_path)
    if not output_dir:
        output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for name, direction in views:
        try:
            # 1. DXF Export using projectToDXF
            dxf_path = os.path.join(output_dir, f"benchy_{name}.dxf")
            # For FreeCAD 0.21, TechDraw.projectToDXF returns a string of the DXF content
            dxf_content = TechDraw.projectToDXF(body.Shape, direction)
            with open(dxf_path, "w") as f:
                f.write(dxf_content)
            print(f"Exported {name} view to {dxf_path}")

            # 2. SVG Export using projectToSVG
            svg_path = os.path.join(output_dir, f"benchy_{name}.svg")
            # TechDraw.projectToSVG returns a string of the SVG content
            svg_str = TechDraw.projectToSVG(body.Shape, direction)
            with open(svg_path, "w") as f:
                f.write(svg_str)
            print(f"Exported {name} view to {svg_path}")

        except Exception as e:
            print(f"Error exporting {name} view: {e}")

    print("Report generation completed.")

if __name__ == "__main__":
    # Check common locations for benchy.FCStd
    possible_paths = [
        "output/benchy.FCStd",
        "benchy.FCStd"
    ]

    doc_file = None
    for path in possible_paths:
        if os.path.exists(path):
            doc_file = path
            break

    if doc_file:
        generate_reports(os.path.abspath(doc_file))
    else:
        print("Error: benchy.FCStd not found in any of the expected locations.")
        sys.exit(1)
