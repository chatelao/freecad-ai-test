# Output Validation Schemas

## SVG Validation
- Must start with `<?xml version="1.0" encoding="UTF-8" standalone="no"?>`.
- Must contain a valid `<svg>` tag with `xmlns="http://www.w3.org/2000/svg"`.
- Must be viewable in standard web browsers.

## DXF Validation
- Must be a valid DXF file (ASCII or Binary).
- Should be importable by CAD software (FreeCAD, AutoCAD, etc.).

## PDF Validation
- Must start with `%PDF-`.
- Must contain the exported views from the model.

## STL Validation
- Must be a valid STL file (Binary preferred).
- No holes or non-manifold edges.
- Bounding box must match specifications within 0.5%.
