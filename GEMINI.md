# Goal
Draw a Benchy with FreeCAD augmented with MCP, keep the 3d files and STLs for 3D printing.

# Locations
- `/` : Store the result a FreeCAD, SCAD and .stl file.
- `/specifications` : Store relevant files, convert to .md if necessary.
- `/specifications` : Include SVG, DXF and PDF file format specifications and schemas for output validations.
- `/images` : Open-Source of the objects like drawing, fotos, etc.
- `/design` : Store designs / thinking steps to be reused later, delete if obsolete.
- `/tools` : Store scripts and other tools, delete if only of temporary value.

# Technical Specifications
- **Horizontal overall-length:** 60.00 mm
- **Horizontal overall-width:** 31.00 mm
- **Vertical overall-height:** 48.00 mm
- **Bridge roof length:** 23.00 mm
- **Chimney roundness:** 3.00 mm (inner diameter), 7.00 mm (outer diameter), 11.00 mm (depth)
- **Cargo-box size:** 12.00 x 10.81 mm (outside), 8.00 x 7.00 mm (inside), 9.00 mm (depth)
- **Hawsepipe diameter:** 4.00 mm (inner diameter), 0.30 mm (flange depth)
- **Bridge front window size:** 10.50 x 9.50 mm
- **Bridge rear window size:** 9.00 mm (inner diameter), 12.00 mm (outer diameter), 0.30 mm (flange depth)
- **Bow overhang inclination:** 40°
- **Bridge roof inclination:** 5.5°
- **Small-detail stern nameplate:** 0.10 mm extrusion

# Howto
1. Create a FreeCAD and a SCAD version of the models.
2. Export files for each the top, front and the side view of each part and the whole model. Be sure to have the Model centered on the sheet.
3. Compare the six views with your expectation.
4. Render each model from 6 random views and compare to the usual views of the boat.
5. Verify all ".svg" have the valid XML headers as defined by the standard.
6. Be sure there are not unwanted gaps, but all wanted gaps and holes are present.
7. Ensure each model is at least 99.5% accurate compared to the Technical Specifications.
8. Use MeshLab for deep inspection of both resulting .stl models.
9. Ensure both model shapes and extract the best solutions from solutions.
10. Be sure to keep it a good looking boat for the human eye.
11. Fix the gaps and deviations in the 3D model and repeeat the validation on step 1 for three times.
12. Once satisfied, export the final model and the top, front and side view into a PDF.

# See / Use
- https://github.com/jango-blockchained/mcp-freecad (Should be installed, read to run)
- https://freecad.github.io/SourceDoc/modules.html
- https://wiki.freecad.org/Power_users_hub#General
