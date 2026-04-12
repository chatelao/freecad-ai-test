# 3DBenchy Output Validation Checklist

## Dimensions (Tolerance +/- 0.5%)
- [ ] **Overall Length:** 60.00 mm (Min: 59.7mm, Max: 60.3mm)
- [ ] **Overall Width:** 31.00 mm (Min: 30.845mm, Max: 31.155mm)
- [ ] **Overall Height:** 48.00 mm (Min: 47.76mm, Max: 48.24mm)
- [ ] **Bridge Roof Length:** 23.00 mm
- [ ] **Chimney:** 3.00 mm ID, 7.00 mm OD, 11.00 mm depth
- [ ] **Cargo-box:** 12.00 x 10.81 mm (outer), 8.00 x 7.00 mm (inner), 9.00 mm depth
- [ ] **Hawsepipe:** 4.00 mm ID, 0.30 mm flange
- [ ] **Bridge front window:** 10.50 x 9.50 mm
- [ ] **Bridge rear window:** 9.00 mm ID, 12.00 mm OD, 0.30 mm flange
- [ ] **Bow overhang:** 40°
- [ ] **Bridge roof inclination:** 5.5°
- [ ] **Stern nameplate:** 0.10 mm extrusion

## File Formats
- [ ] **FreeCAD:** `benchy.fcstd` (centered)
- [ ] **OpenSCAD:** `benchy.scad`
- [ ] **STL:** `benchy.stl`
- [ ] **SVG:** Top, Front, Side views (valid XML headers, centered)
- [ ] **DXF:** Top, Front, Side views
- [ ] **PDF:** Combined report with top, front, and side views.

## Quality Checks
- [ ] No unwanted gaps.
- [ ] All specified holes are present.
- [ ] Good aesthetics for human eye.
- [ ] 6 random view renders for visual comparison.
- [ ] Bounding box verification script passed.
