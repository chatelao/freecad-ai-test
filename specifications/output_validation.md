# Output Validation Schema

## SVG Validation
- File must be valid XML.
- Must contain a `<svg>` root element.
- Should contain paths or shapes representing the projected view.

## DXF Validation
- File must be a valid DXF (binary or ASCII).
- Should contain layers for visible and hidden lines.

## PDF Validation
- File must be a valid PDF.
- Must contain the top, front, and side views.
- Must contain 6 random perspective views.
- Must include the final model name and date.

## Accuracy Threshold
- Dimensions must be within 99.5% of the specifications in `benchy_specs.md`.
