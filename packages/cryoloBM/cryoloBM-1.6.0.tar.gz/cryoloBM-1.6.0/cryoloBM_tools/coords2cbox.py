from cryoloBM.bmtool import BMTool
from argparse import ArgumentParser
import argparse
from typing import List
import numpy as np
from cryolo.utils import Filament, BoundBox
from cryolo.CoordsIO import read_cbox_boxfile
from glob import glob
from cryolo.CoordsIO import write_cbox_file

import os

class Coords2CBOX(BMTool):

    def get_command_name(self) -> str:
        '''
        :return: Command name
        '''
        return "coords2cbox"

    def create_parser(self, parentparser: ArgumentParser) -> ArgumentParser:
        helptxt = "Converts .coords files to .cbox files."
        parser = parentparser.add_parser(
            self.get_command_name(),
            help=helptxt,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )

        req = parser.add_argument_group(
            "Arguments",
            helptxt,
        )

        req.add_argument(
            "-i",
            "--input",
            required=True,
            help="Path to folder with .coords files / path to single .coords file ",
        )

        req.add_argument(
            "-b",
            "--boxsize",
            type=int,
            required=True,
            help="Boxsize",
        )

        req.add_argument(
            "--fid_first",
            action='store_true',
            default=False,
            help="Set this flag, when filament is in the first column",
        )

        req.add_argument(
            "-o",
            "--out",
            required=True,
            help="Output path",
        )

    @staticmethod
    def coords_to_filaments(data : np.array) -> List[Filament]:
        fils = []
        for id in np.unique(data[:,3]):
            boxes = []
            for row in data[data[:,3]==id]:
                x = row[0]
                y = row[1]
                z = row[2]
                boxes.append(BoundBox(x=x,y=y,z=z,h=0,w=0))
            f = Filament(boxes)
            f.meta["fid"] = id
            fils.append(f)
        return fils

    def has_filament_id(self, coords):
        return coords.shape[1] == 4

    @staticmethod
    def coords2boundingbox(coords: np.array, boxsize: int) -> List[BoundBox]:
        boxes = []
        for row in coords:
            x = row[0] - boxsize/2
            y = row[1] - boxsize/2
            z = row[2]
            boxes.append(BoundBox(x=x, y=y, z=z, h=boxsize, w=boxsize, depth=boxsize))
        return boxes

    @staticmethod
    def read_coords(path) -> np.array:
        return np.atleast_2d(np.genfromtxt(path))

    def _run(self, input_path: str,
             output_path: str,
             boxsize: int,
             fid_first:bool = False):
        os.makedirs(output_path, exist_ok=True)

        input_files = []
        if os.path.isfile(input_path):
            input_files.append(input_path)
        else:
            input_files = glob(os.path.join(input_path, "*.coords"))

        for file in input_files:
            coords = Coords2CBOX.read_coords(file)
            if coords.size==0:
                print("No coordinates found in ", file)
                continue

            if self.has_filament_id(coords):
                if fid_first:
                    coords = np.roll(coords,3,axis=1) #make fid last
                boxes = Coords2CBOX.coords_to_filaments(coords)
            else:
                boxes = Coords2CBOX.coords2boundingbox(coords, boxsize=boxsize)

            filename = os.path.splitext(os.path.basename(file))[0]
            outpth = os.path.join(output_path, filename + ".cbox")
            write_cbox_file(path=outpth, coordinates=boxes)


    def run(self, args):
        input_path = args.input
        output_path = args.out
        boxsize = args.boxsize
        self._run(input_path,output_path,boxsize, args.fid_first)




