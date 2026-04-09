// 3DBenchy OpenSCAD model (Approximation)

module benchy() {
    // Hull
    hull() {
        translate([-20, -5, 0]) cube([30, 10, 0.1]);
        translate([-25, -12, 8]) cube([40, 24, 0.1]);
        translate([-30, -15.5, 15.5]) cube([60, 31, 0.1]);
    }

    // Deck
    translate([-28, -14, 14]) cube([45, 28, 2]);

    // Cabin
    difference() {
        translate([-10, -9, 15.5]) cube([20, 18, 20]);
        // Front Window
        translate([9, -5.25, 22]) cube([2, 10.5, 9.5]);
        // Side Windows
        translate([-5, 8, 22]) cube([10, 2, 8]);
        translate([-5, -10, 22]) cube([10, 2, 8]);
    }

    // Roof
    translate([-12, -11, 35.5])
    rotate([0, -5.5, 0])
    cube([23, 22, 2]);

    // Chimney
    translate([5, 0, 34])
    difference() {
        cylinder(h=14, r=3.5, $fn=32);
        translate([0, 0, 3]) cylinder(h=11.1, r=1.5, $fn=32);
    }

    // Cargo Box
    translate([-25, -5.405, 15.5])
    difference() {
        cube([12, 10.81, 9]);
        translate([2, 1.905, 1]) cube([8, 7, 9]);
    }
}

benchy();
