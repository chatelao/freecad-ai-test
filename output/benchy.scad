
// 3DBenchy in OpenSCAD

module hull() {
    difference() {
        cube([60, 31, 15]);

        // Taper bow
        translate([30, 0, -1])
            rotate([0, 0, atan2(15.5, 30)])
                translate([0, -20, 0])
                    cube([40, 20, 17]);

        translate([30, 31, -1])
            rotate([0, 0, -atan2(15.5, 30)])
                cube([40, 20, 17]);

        // Deck recess
        translate([2, 2, 12])
            cube([50, 27, 5]);
    }
}

module cabin() {
    difference() {
        translate([15, 5.5, 12])
            cube([20, 20, 20]);

        // Front window
        translate([34, 9.5, 18])
            cube([2, 12, 10]);
    }
}

module chimney() {
    difference() {
        translate([28, 15.5, 32])
            cylinder(h=15, r=3.5, $fn=32);

        translate([28, 15.5, 31])
            cylinder(h=17, r=1.5, $fn=32);
    }
}

union() {
    hull();
    cabin();
    chimney();
}
