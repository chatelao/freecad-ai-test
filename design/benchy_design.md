# Benchy Design Strategy

The 3DBenchy will be constructed using programmatically defined geometry in FreeCAD's Python API.

## 1. Hull Construction
- **Method**: Lofting between multiple profiles.
- **Profiles**:
    - **Bottom**: Small rounded rectangle (approx. 36x15mm).
    - **Mid-section**: Widest part (approx. 60x31mm at the deck level).
    - **Top**: Gunwale curve.
- **Bow**: The front points of the profiles will converge to form the bow, with a 40-degree overhang.

## 2. Deck and Cargo Box
- **Deck**: A flat surface at a specific height (approx. 12mm-15.5mm).
- **Cargo Box**: A rectangular pocket or extrusion at the stern (12x12x9mm).

## 3. Cabin
- **Main Box**: 23x23mm base, extruded 21mm high.
- **Windows**: Subtracted boxes or cylinders from the cabin walls.
- **Roof**: A slightly larger plate (24x26mm) with a 5.5-degree inclination.

## 4. Chimney and Details
- **Chimney**: Cylinder with 7mm OD and 3mm ID, 11mm height.
- **Stern Nameplate**: Rectangular area for the name.

## 5. Assembly Strategy
- All parts will be created as `Part.Feature` objects and then combined using a boolean union (`Part.makeCompound` or `Part.BOPTools`).
- The final shape will be exported as STL and FCStd.

## 6. Geometric Constraints
- **Length**: 60.0mm (+/- 0.3mm)
- **Width**: 31.0mm (+/- 0.3mm)
- **Height**: 48.0mm (+/- 0.3mm)
- **Accuracy Target**: 99.5%
