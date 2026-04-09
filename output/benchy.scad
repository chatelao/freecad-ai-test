
// 3DBenchy OpenSCAD version

module hull() {
    hull() {
        translate([-20, 0, 0]) sphere(r=1);
        translate([15, 7, 0]) sphere(r=1);
        translate([28, 0, 0]) sphere(r=1);
        translate([15, -7, 0]) sphere(r=1);

        translate([-25, 0, 10]) sphere(r=1);
        translate([15, 15.5, 10]) sphere(r=1);
        translate([30, 0, 10]) sphere(r=1);
        translate([15, -15.5, 10]) sphere(r=1);

        translate([-30, 0, 15]) sphere(r=1);
        translate([10, 15, 15]) sphere(r=1);
        translate([30, 0, 15]) sphere(r=1);
        translate([10, -15, 15]) sphere(r=1);
    }
}

module deck() {
    translate([-15, -14, 15]) cube([35, 28, 2]);
}

module cabin() {
    difference() {
        translate([-10, -10, 17]) cube([20, 20, 20]);
        translate([-9, -9, 18]) cube([18, 18, 20]);
    }
    // Roof
    translate([-11, -11, 37]) cube([22, 22, 2]);
}

module chimney() {
    translate([0, 0, 39]) cylinder(r=3, h=10);
}

// Assemble
union() {
    hull();
    deck();
    cabin();
    chimney();
}
