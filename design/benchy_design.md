# 3DBenchy Design Plan

The 3DBenchy will be constructed using geometric primitives and boolean operations in FreeCAD and OpenSCAD.

## Components

### 1. Hull
- **Main Body**: A loft or a series of sections to create the boat shape.
- **Bow**: Pointed front with 40° overhang.
- **Stern**: Rounded rear.
- **Dimensions**: Length ~60mm, Width ~31mm.

### 2. Deck
- Flat surface inside the hull.
- Includes a small cargo box at the rear.

### 3. Cabin
- Rectangular base with windows.
- **Roof**: Inclined at 5.5°.
- **Door**: Arched opening at the back.

### 4. Chimney
- Cylindrical shape.
- **Diameter**: 7.00 mm.
- **Height**: 11.00 mm.

### 5. Details
- Steering wheel (simplified).
- Nameplate area on the stern.

## Construction Method (FreeCAD)
- Use `PartDesign` workbench.
- Create a `Body`.
- Use `Addictive` and `Subtractive` primitives.
- Use `Loft` for the complex hull shape.

## Construction Method (OpenSCAD)
- Use `union()`, `difference()`, and `intersection()`.
- Use `hull()` for the boat body.
- Use `cylinder()`, `cube()`, and `polyhedron()`.
