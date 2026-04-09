
// 3DBenchy in OpenSCAD

$fn = 50;

L = 60.0;
W = 31.0;
H = 48.0;
DECK_H = 15.5;
BOW_ANGLE = 40.0;
ROOF_ANGLE = 5.5;

module ship_hull() {
    hull() {
        // Stern bottom
        translate([0, -31*0.6/2, 0]) cube([0.1, 31*0.6, 0.1]);
        // Bow bottom
        translate([60 - (15.5 / tan(40)), 0, 0]) cylinder(h=0.1, r=0.1);
        // Stern deck
        translate([0, -31/2, 15.5]) cube([0.1, 31, 0.1]);
        // Bow deck
        translate([60, 0, 15.5]) cylinder(h=0.1, r=0.1);
    }
}

module cargo_box() {
    translate([5, -10.81/2, 15.5])
    difference() {
        cube([12, 10.81, 9]);
        translate([2, 1.905, 1]) cube([8, 7, 9]);
    }
}

module cabin() {
    cabin_l = 23;
    cabin_w = 22;
    cabin_h = 20;
    cabin_x = 22;

    translate([cabin_x, -cabin_w/2, 15.5])
    difference() {
        cube([cabin_l, cabin_w, cabin_h]);
        // Sloped roof cut
        rotate([0, ROOF_ANGLE, 0])
        translate([-5, -1, cabin_h])
        cube([cabin_l + 10, cabin_w + 2, 10]);

        // Front window
        translate([cabin_l - 2, (cabin_w - 10.5)/2, 5])
        cube([5, 10.5, 9.5]);
    }
}

module chimney() {
    translate([27, 0, 33])
    difference() {
        cylinder(h=15, r=3.5);
        translate([0, 0, 4]) cylinder(h=12, r=1.5);
    }
}

union() {
    ship_hull();
    cargo_box();
    cabin();
    chimney();
}
