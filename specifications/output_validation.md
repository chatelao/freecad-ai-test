# Output Validation Schema

Each exported file must meet the following criteria:

## STL Validation
- **Bounding Box**: Must be within 0.5% of 60x31x48 mm.
- **Manifold**: Must be a closed manifold (no holes).
- **Format**: Binary or ASCII STL.

## FreeCAD (.FCStd) Validation
- **Hierarchy**: Logical naming of parts (Hull, Cabin, etc.).
- **Parametric**: Dimensions should be easily adjustable.

## SVG/DXF Validation
- **Views**: Must include Top, Front, and Side views.
- **Scale**: Should be 1:1 if possible, or clearly labeled.

## PDF Report
- **Content**: Must include the 3 standard views and 6 random perspective views.
- **Metadata**: Title, Date, and Version.
