import os

def generate_scad():
    scad_content = """/**
 * 3DBenchy in OpenSCAD
 */

// Dimensions
L = 60;
W = 31;
H = 48;

module hull_body() {
    hull() {
        // Bottom
        translate([5, -5, 0]) cube([35, 10, 0.1]);
        translate([55, 0, 0]) cube([0.1, 0.1, 0.1], center=true);

        // Deck level
        translate([0, -15.5, 15]) cube([40, 31, 0.1]);
        translate([60, 0, 15]) cube([0.1, 0.1, 0.1], center=true);
    }
}

module deck() {
    translate([10, -13, 13]) cube([40, 26, 2]);
}

module cabin() {
    // Body
    translate([15, -10, 15]) cube([20, 20, 15]);

    // Roof
    translate([12.5, -12, 30]) {
        cube([25, 24, 7]);
    }
}

module chimney() {
    translate([25, 0, 37]) cylinder(h=11, d=7, $fn=32);
}

module benchy() {
    union() {
        hull_body();
        deck();
        cabin();
        chimney();
    }
}

benchy();
"""
    if not os.path.exists("output"):
        os.makedirs("output")

    with open("output/benchy.scad", "w") as f:
        f.write(scad_content)

    print("OpenSCAD file generated at output/benchy.scad")

if __name__ == "__main__":
    generate_scad()
