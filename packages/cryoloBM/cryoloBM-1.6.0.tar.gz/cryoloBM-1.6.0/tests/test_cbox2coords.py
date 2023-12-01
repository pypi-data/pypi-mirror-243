import unittest
from cryoloBM_tools import coords2cbox
from cryolo import CoordsIO
from cryolo.utils import Filament

import tempfile
import os
from glob import glob
from typing import List

class MyTestCase(unittest.TestCase):
    def test_convert_to_cbox_particle(self):
        input_path = os.path.join(os.path.dirname(__file__),
                                  "../resources/coords_data/example.coords")
        tool = coords2cbox.Coords2CBOX()
        with tempfile.TemporaryDirectory() as outputdir:
            tool._run(input_path, outputdir,30)
            files = glob(outputdir+"/*.cbox")
            boxes = CoordsIO.read_cbox_boxfile(files[0])
            num_boxes = len(boxes)

        self.assertEqual(num_boxes, 958)  # add assertion here

    def test_convert_to_cbox_filament_fidlast(self):
        input_path = os.path.join(os.path.dirname(__file__),
                                  "../resources/coords_data/coords_with_fid_simple_fidlast.coords")
        tool = coords2cbox.Coords2CBOX()
        with tempfile.TemporaryDirectory() as outputdir:
            tool._run(input_path, outputdir,30)
            files = glob(outputdir+"/*.cbox")
            filaments: List[Filament] = CoordsIO.read_cbox_boxfile(files[0])
            num_fil = len(filaments)

        self.assertEqual(num_fil, 2)  # add assertion here
        self.assertAlmostEqual(filaments[0].boxes[-1].x - 193.660170, 0)

    def test_convert_to_cbox_filament_fidfirst(self):
        input_path = os.path.join(os.path.dirname(__file__),
                                  "../resources/coords_data/coords_with_fid_simple_fidfirst.coords")
        tool = coords2cbox.Coords2CBOX()
        with tempfile.TemporaryDirectory() as outputdir:
            tool._run(input_path, outputdir,30, fid_first=True)
            files = glob(outputdir+"/*.cbox")
            filaments: List[Filament] = CoordsIO.read_cbox_boxfile(files[0])
            print("x:", filaments[0].boxes[0].x)
            num_fil = len(filaments)

        self.assertEqual(num_fil, 2)  # add assertion here
        self.assertAlmostEqual(filaments[0].boxes[-1].x - 193.660170, 0)


if __name__ == '__main__':
    unittest.main()
