import sys
import os

# Use the discovery utility to set up the FreeCAD environment.
try:
    from freecad_utils import setup_freecad
    if not setup_freecad():
        print("FreeCAD environment setup failed.")
        sys.exit(1)
except ImportError:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(script_dir)
    from freecad_utils import setup_freecad
    if not setup_freecad():
         print("FreeCAD environment setup failed.")
         sys.exit(1)

import FreeCAD
import TechDraw

def generate_report():
    # Load the document
    output_dir = "output"
    fcstd_file = os.path.join(output_dir, "benchy.fcstd")

    if not os.path.exists(fcstd_file):
        print(f"Error: {fcstd_file} not found. Please run draw_benchy.py first.")
        sys.exit(1)

    doc = FreeCAD.open(fcstd_file)
    benchy_obj = doc.getObject("BenchyModel")

    if not benchy_obj:
        print("Error: BenchyModel object not found in document.")
        sys.exit(1)

    # Create a TechDraw Page
    page = doc.addObject("TechDraw::DrawPage", "Page")

    # Locate a template (A4 Landscape)
    template_paths = [
        "/usr/share/freecad/Mod/TechDraw/Templates/A4_LandscapeTD.svg",
        "/usr/share/freecad/Mod/TechDraw/Templates/A4_Landscape_ISO7200TD.svg"
    ]
    template_path = ""
    for p in template_paths:
        if os.path.exists(p):
            template_path = p
            break

    # Create a template object
    template = doc.addObject("TechDraw::DrawSVGTemplate", "Template")
    if template_path:
        template.Template = template_path
    page.Template = template

    # 1. Top View (Looking down Z)
    view_top = doc.addObject("TechDraw::DrawViewPart", "TopView")
    view_top.Source = [benchy_obj]
    view_top.Direction = (0, 0, 1)
    view_top.X = 100
    view_top.Y = 150
    page.addView(view_top)

    # 2. Front View (Looking along X)
    view_front = doc.addObject("TechDraw::DrawViewPart", "FrontView")
    view_front.Source = [benchy_obj]
    view_front.Direction = (1, 0, 0)
    view_front.X = 180
    view_front.Y = 100
    page.addView(view_front)

    # 3. Side View (Looking along Y)
    view_side = doc.addObject("TechDraw::DrawViewPart", "SideView")
    view_side.Source = [benchy_obj]
    view_side.Direction = (0, 1, 0)
    view_side.X = 100
    view_side.Y = 50
    page.addView(view_side)

    # Update document to generate views
    doc.recompute()

    # Exporting
    # Try multiple ways to export SVG since TechDrawGui is not reliable in headless console
    try:
        page_file_svg = os.path.join(output_dir, "benchy_report.svg")
        import TechDrawGui
        # Attempt TechDrawGui if possible
        try:
             TechDrawGui.exportPageAsSvg(page, page_file_svg)
             print(f"Exported SVG (via TechDrawGui): {page_file_svg}")
        except Exception:
             raise ImportError
    except (ImportError, AttributeError):
        # Fallback to direct attribute extraction if available
        svg_content = ""
        # Inspecting the object for SVG-like strings
        for prop in page.PropertiesList:
             try:
                 val = getattr(page, prop)
                 if isinstance(val, str) and "<svg" in val:
                      svg_content = val
                      break
             except Exception:
                 continue

        if not svg_content:
             # In some versions, calling page.dumpContent() might help but it returns a string
             # Usually the page object has some way to get its result.
             # Let's try to export the Template at least as a starting point if views fail
             if page.Template and hasattr(page.Template, "Template"):
                  try:
                      with open(page.Template.Template, 'r') as f:
                           svg_content = f.read()
                  except Exception:
                      pass

        if svg_content:
            with open(page_file_svg, "w") as f:
                 f.write(svg_content)
            print(f"Exported SVG (via fallback): {page_file_svg}")
        else:
            print("Warning: Could not export SVG in this environment.")

    # Export to DXF (individual view) - This usually works in console mode
    try:
        page_file_dxf = os.path.join(output_dir, "benchy_report.dxf")
        TechDraw.writeDXFView(view_side, page_file_dxf)
        print(f"Exported DXF: {page_file_dxf}")
    except Exception as e:
        print(f"DXF Export Error: {e}")

    # Save the document again with TechDraw page
    doc.save()
    print("Report generation attempt completed.")

if __name__ == "__main__":
    generate_report()
