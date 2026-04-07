import sys
import os
from freecad_utils import setup_freecad, get_template_path

def generate_report():
    import FreeCAD
    import Part
    import TechDraw

    fcstd_path = "output/benchy.FCStd"
    if not os.path.exists(fcstd_path):
        print(f"Error: {fcstd_path} not found.")
        return False

    doc = FreeCAD.openDocument(fcstd_path)

    # Create TechDraw Page
    page = doc.addObject("TechDraw::DrawPage", "Page")
    template = doc.addObject("TechDraw::DrawSVGTemplate", "Template")

    template.Template = get_template_path()
    page.Template = template

    # Define objects to view
    objects_to_view = ["BenchyFull", "Hull", "BowPart", "Deck", "CabinFinal", "Roof", "Chimney", "CargoBox"]

    # Layout configuration for A4 Landscape (approx 297x210 mm)
    y_start = 180
    x_start = 40
    spacing_x = 70
    spacing_y = 22 # Reduced spacing to fit more rows
    scale = 0.5    # Scaled down to fit

    for i, obj_name in enumerate(objects_to_view):
        obj = doc.getObject(obj_name)
        if obj is None:
            print(f"Warning: Object {obj_name} not found.")
            continue

        # Front View
        view_front = doc.addObject("TechDraw::DrawViewPart", f"ViewFront_{obj_name}")
        view_front.Source = [obj]
        view_front.Direction = (0, 1, 0)
        view_front.X = x_start
        view_front.Y = y_start - (i * spacing_y)
        view_front.Scale = scale
        page.addView(view_front)

        # Top View
        view_top = doc.addObject("TechDraw::DrawViewPart", f"ViewTop_{obj_name}")
        view_top.Source = [obj]
        view_top.Direction = (0, 0, 1)
        view_top.X = x_start + spacing_x
        view_top.Y = y_start - (i * spacing_y)
        view_top.Scale = scale
        page.addView(view_top)

        # Side View
        view_side = doc.addObject("TechDraw::DrawViewPart", f"ViewSide_{obj_name}")
        view_side.Source = [obj]
        view_side.Direction = (1, 0, 0)
        view_side.X = x_start + 2 * spacing_x
        view_side.Y = y_start - (i * spacing_y)
        view_side.Scale = scale
        page.addView(view_side)

    doc.recompute()

    # Export PDF using TechDrawGui if possible
    try:
        import FreeCADGui
        import TechDrawGui
        # Ensure Gui is started
        FreeCADGui.showMainWindow()
        output_pdf = "output/benchy_report.pdf"
        TechDrawGui.exportPageAsPdf(page, output_pdf)
        print(f"PDF report exported to {output_pdf}")
    except Exception as e:
        print(f"TechDrawGui not available for PDF export: {e}")
        doc.save()
        print("Document saved with TechDraw page.")

    return True

if __name__ == "__main__":
    if setup_freecad():
        if generate_report():
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        sys.exit(1)
