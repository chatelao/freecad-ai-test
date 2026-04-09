# Output Validation Requirements

## STL File (.stl)
- Must be watertight (no gaps).
- Bounding box must be 60.00 x 31.00 x 48.00 mm (+/- 0.5% as per requirements).
- Unit of measurement: Millimeters (mm).

## SVG Files (.svg)
- Must start with valid XML header: `<?xml version="1.0" encoding="UTF-8" standalone="no"?>`.
- Must contain valid `<svg ...>` tag.
- Views required:
  - Top View
  - Front View
  - Side View (Right or Left)
  - 6 Random Views

## DXF Files (.dxf)
- Views required:
  - Top View
  - Front View
  - Side View

## PDF Report (.pdf)
- Must aggregate the Top, Front, and Side views.
- Should include the Random views if possible.
- Should display the model name and basic dimensions.

## General Accuracy
- The models (FreeCAD and SCAD) must be at least 99.5% accurate to the 3DBenchy specifications.
