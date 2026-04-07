import sys
import os
from freecad_utils import setup_freecad

if __name__ == "__main__":
    if setup_freecad():
        import FreeCAD
        import Part
        import Mesh

        def draw_benchy():
            doc = FreeCAD.newDocument("Benchy")

            # 1. Hull
            # Total length 60, width 31, height 15
            # Bow len ~18 for 40 deg overhang
            bow_len = 18.0
            hull_main_len = 60.0 - bow_len

            # Main Hull
            hull_main = doc.addObject("Part::Box", "Hull")
            hull_main.Length = hull_main_len
            hull_main.Width = 31
            hull_main.Height = 15
            hull_main.Placement = FreeCAD.Placement(FreeCAD.Vector(bow_len, -15.5, 0), FreeCAD.Rotation(0, 0, 0))

            # Symmetric Bow using Wedge
            # Xmin, Ymin, Zmin, Xmax, Ymax, Zmax, X2min, Z2min, X2max, Z2max
            bow = doc.addObject("Part::Wedge", "BowPart")
            bow.Xmin = 0; bow.Ymin = -15.5; bow.Zmin = 0
            bow.Xmax = bow_len; bow.Ymax = 15.5; bow.Zmax = 15
            bow.X2min = bow_len; bow.Z2min = 15; bow.X2max = bow_len; bow.Z2max = 15

            # 2. Deck
            deck = doc.addObject("Part::Box", "Deck")
            deck.Length = 45
            deck.Width = 31
            deck.Height = 2
            deck.Placement = FreeCAD.Placement(FreeCAD.Vector(15, -15.5, 15), FreeCAD.Rotation(0, 0, 0))

            # 3. Cabin
            cabin_box = doc.addObject("Part::Box", "CabinPart")
            cabin_box.Length = 25
            cabin_box.Width = 20
            cabin_box.Height = 18
            cabin_box.Placement = FreeCAD.Placement(FreeCAD.Vector(25, -10, 17), FreeCAD.Rotation(0, 0, 0))

            # Window cut-outs
            window_l = doc.addObject("Part::Box", "WindowL")
            window_l.Length = 10; window_l.Width = 5; window_l.Height = 10
            window_l.Placement = FreeCAD.Placement(FreeCAD.Vector(30, -12, 22), FreeCAD.Rotation(0, 0, 0))

            window_r = doc.addObject("Part::Box", "WindowR")
            window_r.Length = 10; window_r.Width = 5; window_r.Height = 10
            window_r.Placement = FreeCAD.Placement(FreeCAD.Vector(30, 7, 22), FreeCAD.Rotation(0, 0, 0))

            cabin_cut1 = doc.addObject("Part::Cut", "CabinCut1")
            cabin_cut1.Base = cabin_box
            cabin_cut1.Tool = window_l
            doc.recompute()
            cabin_final = doc.addObject("Part::Cut", "CabinFinal")
            cabin_final.Base = cabin_cut1
            cabin_final.Tool = window_r

            # 4. Roof with 5.5 degree inclination
            roof = doc.addObject("Part::Box", "Roof")
            roof.Length = 28
            roof.Width = 24
            roof.Height = 2
            # 5.5 degree around Y
            roof.Placement = FreeCAD.Placement(FreeCAD.Vector(24, -12, 35), FreeCAD.Rotation(FreeCAD.Vector(0,1,0), -5.5))

            # 5. Chimney with a hole
            chim_outer = doc.addObject("Part::Cylinder", "ChimneyOuter")
            chim_outer.Radius = 4
            chim_outer.Height = 11
            chim_outer.Placement = FreeCAD.Placement(FreeCAD.Vector(35, 0, 37), FreeCAD.Rotation(0, 0, 0))

            chim_inner = doc.addObject("Part::Cylinder", "ChimneyInner")
            chim_inner.Radius = 2.5
            chim_inner.Height = 12
            chim_inner.Placement = FreeCAD.Placement(FreeCAD.Vector(35, 0, 37), FreeCAD.Rotation(0, 0, 0))

            chimney = doc.addObject("Part::Cut", "Chimney")
            chimney.Base = chim_outer
            chimney.Tool = chim_inner

            # 6. Cargo Box at Stern
            cargo_box = doc.addObject("Part::Box", "CargoBox")
            cargo_box.Length = 10
            cargo_box.Width = 20
            cargo_box.Height = 5
            cargo_box.Placement = FreeCAD.Placement(FreeCAD.Vector(45, -10, 17), FreeCAD.Rotation(0, 0, 0))

            doc.recompute()

            # Combined Benchy
            benchy_fusion = doc.addObject("Part::MultiFuse", "BenchyFull")
            benchy_fusion.Shapes = [hull_main, bow, deck, cabin_final, roof, chimney, cargo_box]

            doc.recompute()

            output_dir = "output"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            fcstd_path = os.path.join(output_dir, "benchy.FCStd")
            doc.saveAs(fcstd_path)
            print(f"Document saved to {fcstd_path}")

            stl_path = os.path.join(output_dir, "benchy.stl")
            Mesh.export([benchy_fusion], stl_path)
            print(f"STL exported to {stl_path}")

        draw_benchy()
    else:
        sys.exit(1)
