def generate_scad():
    scad_content = """
// 3DBenchy in OpenSCAD
$fn = 50;

module hull() {
    hull() {
        // Bottom
        translate([0, 0, 0]) cube([30, 16, 0.1], center=true);
        // Mid
        translate([0, 0, 10]) cube([46, 28, 0.1], center=true);
        // Deck
        translate([0, 0, 15]) cube([54.6, 28.02, 0.1], center=true);
    }
}

module cabin() {
    translate([-15, -10, 15]) cube([20, 20, 18]);
}

module roof() {
    translate([-18, -11, 33])
    rotate([0, -5.5, 0])
    cube([23, 22, 2]);
}

module chimney() {
    translate([-5, 0, 33])
    difference() {
        cylinder(h=15, r=3.5);
        translate([0, 0, -1]) cylinder(h=17, r=1.5);
    }
}

module cargo_box() {
    translate([-28, -5.405, 15])
    difference() {
        cube([12, 10.81, 9]);
        translate([2, 1.905, 1]) cube([8, 7, 10]);
    }
}

union() {
    hull();
    cabin();
    roof();
    chimney();
    cargo_box();
}
"""
    with open("benchy.scad", "w") as f:
        f.write(scad_content)
    print("Exported benchy.scad")

if __name__ == "__main__":
    generate_scad()
