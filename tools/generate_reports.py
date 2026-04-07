import sys
import os
from freecad_utils import init_freecad

def generate_reports():
    FreeCAD = init_freecad()
    if not FreeCAD:
        sys.exit(1)

    import TechDraw

    # Ensure output directory exists
    os.makedirs("output/views", exist_ok=True)

    # Re-open the document
    doc_path = "output/benchy.FCStd"
    if not os.path.exists(doc_path):
        doc_path = "benchy.FCStd" # Fallback to root

    if not os.path.exists(doc_path):
        print(f"Error: {doc_path} not found.")
        sys.exit(1)

    doc = FreeCAD.openDocument(doc_path)

    # Select the model (BenchyBody)
    model = doc.getObject("BenchyBody")

    # List of views to generate
    # Name, direction
    views = [
        ("top", FreeCAD.Vector(0, 0, 1)),
        ("front", FreeCAD.Vector(0, -1, 0)),
        ("side", FreeCAD.Vector(1, 0, 0))
    ]

    for name, direction in views:
        # Projection (SVG)
        svg_path = f"output/views/{name}.svg"
        # projectToSVG(shape, direction) returns the SVG string
        svg_content = TechDraw.projectToSVG(model.Shape, direction)
        with open(svg_path, "w") as f:
            f.write(svg_content)
        print(f"Generated {name} SVG to {svg_path}")

    print("Individual 2D views generated. PDF generation skipped due to environment limitations.")

    doc.save()

if __name__ == "__main__":
    generate_reports()
