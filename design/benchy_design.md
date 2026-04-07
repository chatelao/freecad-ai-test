# Programmatic Benchy Design

To create the 3DBenchy model in FreeCAD using Python, I will use a combination of PartDesign and Part workbenches.

## Hierarchy
1. **Hull Body:**
   - Use a lofted feature or primitives to approximate the boat hull.
   - For simplicity, start with a solid block and use boolean operations or Chamfer/Fillet to shape the bow and sides.
2. **Deck:**
   - Create a flat plate on top of the hull.
3. **Cabin:**
   - Use a rectangular block on the deck.
   - Cut out window and door openings.
4. **Roof:**
   - Add a slanted plate on top of the cabin (5.5° inclination).
5. **Chimney:**
   - Add a cylinder on the roof.

## Approach
- Use `FreeCAD.newDocument()` to start.
- Use `Part.makeBox()`, `Part.makeCylinder()`, and `Part.makeCone()` for primitives.
- Use `fuse()` and `cut()` for Boolean operations.
- Set coordinates and rotations explicitly.
- Center the model on the origin for easier alignment.

## Dimensions (Approximate for Programmatic Drawing)
- Hull: 60mm length, 31mm width, 15mm height (before shaping).
- Cabin: 20mm x 20mm x 20mm.
- Chimney: 8mm diameter, 15mm height.
