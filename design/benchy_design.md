# Benchy Design Document

This document outlines the strategy for drawing a 3DBenchy model using FreeCAD's Python API.

## Geometric Components

### 1. Hull
- **Strategy**: Create the hull using a series of cross-sectional sketches and the `Part.makeLoft` function.
- **Key Dimensions**:
  - Length: 60 mm
  - Width: 31 mm
  - Bow Angle: 40°

### 2. Deck
- **Strategy**: A horizontal plane at the top of the hull.
- **Components**:
  - Main deck area.
  - Cargo box: 12.00 x 10.81 mm (outer), 8.00 x 7.00 mm (inner), 9.00 mm deep.

### 3. Cabin (Bridge)
- **Strategy**: Extrude a rectangular base and use boolean operations for windows and the roof.
- **Key Dimensions**:
  - Front window: 10.50 x 9.50 mm.
  - Rear window: 9.00 mm (inner diameter).
  - Roof: 23.00 mm length, 5.5° inclination.

### 4. Chimney
- **Strategy**: Create a cylinder and subtract a smaller cylinder for the hole.
- **Key Dimensions**:
  - Outer Diameter: 7.00 mm.
  - Inner Diameter: 3.00 mm.
  - Depth: 11.00 mm.

### 5. Stern
- **Strategy**: Add a small nameplate at the rear.

## Implementation Details
- Use `Part` module for primitive creation and boolean operations.
- Use `Mesh` module for exporting the final model to STL.
- The script `draw_benchy.py` will encapsulate the creation logic.
- Robust path discovery for FreeCAD library is implemented in all scripts.
