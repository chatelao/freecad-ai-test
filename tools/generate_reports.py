import sys
import os
import random

# Add tools dir to sys.path
sys.path.append(os.path.dirname(__file__))
import freecad_utils
import FreeCAD as App

def generate_reports():
    # Load the FCStd file
    fcstd_file = "benchy.FCStd"
    if not os.path.exists(fcstd_file):
        print(f"Error: {fcstd_file} not found.")
        return

    doc = App.openDocument(fcstd_file)
    obj = doc.getObject("Benchy")
    shape = obj.Shape

    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 1. Standard views
    std_views = freecad_utils.get_std_directions()
    for name, direction in std_views.items():
        svg_path = os.path.join(output_dir, f"view_{name}.svg")
        dxf_path = os.path.join(output_dir, f"view_{name}.dxf")
        freecad_utils.project_to_svg(shape, direction, svg_path)
        freecad_utils.project_to_dxf(shape, direction, dxf_path)
        print(f"Exported {name} views to {output_dir}")

    # 2. 6 Random views
    for i in range(1, 7):
        direction = App.Vector(random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1))
        if direction.Length == 0: direction = App.Vector(0,0,1)
        svg_path = os.path.join(output_dir, f"view_random_{i}.svg")
        freecad_utils.project_to_svg(shape, direction, svg_path)
        print(f"Exported random view {i} to {output_dir}")

    # 3. HTML Report (Proxy for PDF)
    html_content = f"""
    <html>
    <head><title>3DBenchy Report</title></head>
    <body>
    <h1>3DBenchy Report</h1>
    <p>Dimensions: 60x31x48 mm</p>
    <h2>Standard Views</h2>
    <div style="display: flex; flex-wrap: wrap;">
        <div><h3>Top</h3><img src="view_top.svg" width="300"></div>
        <div><h3>Front</h3><img src="view_front.svg" width="300"></div>
        <div><h3>Side</h3><img src="view_side.svg" width="300"></div>
    </div>
    <h2>Random Views</h2>
    <div style="display: flex; flex-wrap: wrap;">
    """
    for i in range(1, 7):
        html_content += f'<div><h3>Random {i}</h3><img src="view_random_{i}.svg" width="200"></div>'

    html_content += """
    </div>
    </body>
    </html>
    """

    with open(os.path.join(output_dir, "report.html"), "w") as f:
        f.write(html_content)
    print(f"Generated HTML report in {output_dir}/report.html")

if __name__ == "__main__":
    generate_reports()
