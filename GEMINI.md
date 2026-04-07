# Goal
Draw a Benchy with FreeCAD, keep the 3d files and STLs for 3D printing.

# Locations
- `/` : Store the result a FreeCAD and .stl file.
- `/specifications` : Store relevant files, convert to .md if necessary.
- `/design` : Store designs / thinking steps to be reused later, delete if obsolete.
- `/tools` : Store scripts and other tools, delete if only of temporary value.

# Howto
1. Create a FreeCAD version of the models.
2. Export seperate valid DXF and PDF files for the top, front and side view of each part and the whole model.
3. Compare the three DXF and PDF 2D views with your knowledge of the expected elements in each of these perspective.
4. Fix the gaps to your expectations in the original 3D model and restart the validation on step 1.
5. Once satisfied, export the final model and its three 2D views into a nice single PDF.

# See
- https://freecad.github.io/SourceDoc/modules.html
- https://wiki.freecad.org/Power_users_hub#General
