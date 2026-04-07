# Benchy Design Process

The Benchy model is generated using a Python script that leverages the FreeCAD `Part` module. This approach allows for programmatic control over the dimensions and positioning of each component.

## Modeling Approach
1. **Hull**: Created by fusing a rectangular box (stern) with a wedge primitive (bow). The bow is designed to approximate the characteristic 40° overhang.
2. **Cabin (Bridge)**: A rectangular box positioned on the deck. Windows are created using the `cut` operation with box and cylinder primitives.
3. **Roof**: A thin box rotated by 5.5° to match the specified inclination.
4. **Chimney**: A hollowed cylinder created by subtracting a smaller cylinder from a larger one.
5. **Cargo Box**: A box with a pocket, created using the `cut` operation.

## Key Primitives Used
- `Part.makeBox`: For the main hull, cabin, roof, and cargo box.
- `Part.makeWedge`: For the bow of the hull.
- `Part.makeCylinder`: For the chimney and rear window.
- `Part.fuse` and `Part.cut`: For Boolean operations to combine or subtract shapes.

## Scripts
- `tools/draw_benchy.py`: The main script for generating the 3D model.
- `tools/verify_benchy.py`: A script to verify the bounding box dimensions.
- `tools/generate_reports.py`: A script for creating 2D technical drawings.
