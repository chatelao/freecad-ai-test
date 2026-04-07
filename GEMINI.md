# Goal
Draw a Benchy with FreeCAD.

# Locations
- `/specifications` : Store relevant files, convert to .md if necessary
- `/design` : Store design / thinking steps to be reused later, delete if obsolete

# Implementation
- `draw_benchy.py`: Python script using the FreeCAD API to generate the #3DBenchy model.
- `benchy.FCStd`: FreeCAD document containing the #3DBenchy design.
- `benchy.stl`: Exported STL file for 3D printing.

## Design Details
The implementation follows the official dimensions from [3DBenchy.com](http://www.3dbenchy.com/dimensions/).
- **Hull**: Generated using lofting through multiple sketches to maintain the 40° bow angle and overall length of 60mm.
- **Cargo Box**: Accurate dimensions (12x10.81mm outside, 8x7mm inside, 9mm deep).
- **Cabin**: Includes front and rear windows (10.5x9.5mm front rectangular, 9mm diameter rear cylindrical).
- **Roof**: Inclined at a 5.5° angle.
- **Chimney**: 7mm outer diameter with a 3mm inner hole.
- **Hawsepipe**: 4mm inner diameter pipes on each side of the bow.
