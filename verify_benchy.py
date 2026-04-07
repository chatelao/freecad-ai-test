import sys
import os
from freecad_utils import setup_freecad

if __name__ == "__main__":
    if setup_freecad():
        import FreeCAD
        import Part

        def verify_benchy():
            fcstd_path = "output/benchy.FCStd"
            if not os.path.exists(fcstd_path):
                print(f"Error: {fcstd_path} not found.")
                return False

            doc = FreeCAD.openDocument(fcstd_path)
            benchy_fusion = doc.getObject("BenchyFull")

            if benchy_fusion is None:
                print("Error: BenchyFull object not found in document.")
                return False

            bbox = benchy_fusion.Shape.BoundBox

            length = bbox.XMax - bbox.XMin
            width = bbox.YMax - bbox.YMin
            height = bbox.ZMax - bbox.ZMin

            print(f"Bounding Box: Length={length:.2f}, Width={width:.2f}, Height={height:.2f}")

            expected_length = 60.0
            expected_width = 31.0
            expected_height = 48.0

            tolerance = 1.0 # Allowing some slack for simplified model details

            if abs(length - expected_length) > tolerance or \
               abs(width - expected_width) > tolerance or \
               abs(height - expected_height) > tolerance:
                print("ERROR: Bounding box dimensions do not match specifications!")
                return False
            else:
                print("SUCCESS: Bounding box dimensions match specifications.")
                return True

        if verify_benchy():
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        sys.exit(1)
