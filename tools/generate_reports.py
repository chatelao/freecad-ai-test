import sys
import os

# Import setup_freecad from freecad_utils
sys.path.append(os.path.join(os.path.dirname(__file__)))
from freecad_utils import setup_freecad, get_techdraw_template

if not setup_freecad():
    print("Failed to initialize FreeCAD. Exiting.")
    sys.exit(1)

import FreeCAD
import TechDraw

def generate_reports():
    """
    Generates SVG views (top, front, side) and a final PDF.
    """
    doc = FreeCAD.openDocument("benchy.FCStd")
    benchy_obj = doc.getObject("Benchy")

    if not benchy_obj:
        print("Error: Benchy object not found in benchy.FCStd.")
        return

    # Create a TechDraw page
    template_path = get_techdraw_template()
    if not template_path:
        print("Error: TechDraw template not found.")
        return

    page = doc.addObject('TechDraw::DrawPage', 'Page')
    template = doc.addObject('TechDraw::DrawSVGTemplate', 'Template')
    template.Template = template_path
    page.Template = template

    # Define views
    views_config = [
        {'name': 'TopView', 'direction': (0, 0, 1), 'x': 100, 'y': 200},
        {'name': 'FrontView', 'direction': (0, -1, 0), 'x': 100, 'y': 100},
        {'name': 'SideView', 'direction': (1, 0, 0), 'x': 200, 'y': 100}
    ]

    for config in views_config:
        view = doc.addObject('TechDraw::DrawViewPart', config['name'])
        view.Source = [benchy_obj]
        view.Direction = config['direction']
        view.X = config['x']
        view.Y = config['y']
        page.addView(view)

        # Also export individual SVG files for each view
        # We can use TechDraw.projectToSVG but it's simpler to export the whole page for the PDF
        # To get individual SVG as requested by GEMINI.md:
        try:
            svg_content = TechDraw.projectToSVG(benchy_obj.Shape, FreeCAD.Vector(*config['direction']))
            with open(f"{config['name']}.svg", "w") as f:
                f.write(svg_content)
            print(f"Exported {config['name']}.svg")
        except Exception as e:
            print(f"Failed to export individual SVG for {config['name']}: {e}")

    doc.recompute()

    # Export PDF (using a workaround if exportPageAsPdf is missing)
    output_pdf = "benchy_report.pdf"
    try:
        # Some versions might use this
        page.exportPdf(output_pdf)
        print(f"Exported {output_pdf} via page.exportPdf")
    except AttributeError:
        try:
            # Another common way is through the GUI-less export if available
            import FreeCADGui
            FreeCADGui.showMainWindow()
            # This is complex in headless, so we'll try another way if this fails
            TechDraw.exportPageAsPdf(page, output_pdf)
        except:
            print("Could not export PDF directly. SVG files are available.")

    doc.save()

if __name__ == "__main__":
    generate_reports()
