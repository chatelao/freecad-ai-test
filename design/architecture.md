# 3DBenchy Design Architecture

## Strategy
The 3DBenchy model is built programmatically using Python and the FreeCAD `Part` workbench. The approach uses constructive solid geometry (CSG), combining primitives (boxes, cylinders, wedges) through boolean operations (fuse, cut).

## Components
1. **Hull**:
   - Created from a base box cut with a rotated box to achieve the 40° bow overhang.
   - Hawsepipes are cylindrical cuts at the bow.
2. **Deck**:
   - A flat box placed at the `deck_height` (15.50 mm).
3. **Cargo Box**:
   - Constructed by cutting a smaller box from a larger one.
4. **Bridge (Cabin)**:
   - A rectangular structure with cuts for the front rectangular window and a cylindrical rear window.
5. **Roof**:
   - A box inclined at 5.5° using the `rotate` method.
6. **Chimney**:
   - A cylinder with a smaller cylindrical cut for the blind hole.
7. **Stern Nameplate**:
   - A thin box extrusion at the stern.

## Parameterization
All key dimensions are defined as variables at the beginning of `tools/draw_benchy.py` to ensure easy adjustments and accurate verification.
