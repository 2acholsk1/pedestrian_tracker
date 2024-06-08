#!/usr/bin/env python3

import cv2
from typing import List
class BoundBox:

    def __init__(self, coordinates: List, image: cv2.Mat) -> None:
        self.coordinates_ = coordinates
        self.img_ = image
        self.nodes_ = []
        self.bb_storage_ = []


    def compute_coords(self, coordinates: List) -> None:
        self.x_ = int(float(coordinates[0]))
        self.y_ = int(float(coordinates[1]))
        self.w_ = int(float(coordinates[2]))
        self.h_= int(float(coordinates[3]))

    
    def compute_bb(self) -> None:
        for iter, coords in enumerate(self.coordinates_):
            self.nodes_.append(str(iter))
            self.compute_coords(coords)
            self.bb_storage_.append(self.img_[self.y_ + int(self.h_/4) : self.y_ + int(3*(self.h_)/4),
                                            self.x_ + int(self.w_/4) : self.x_ + int(3*(self.w_)/4)])
    

    def return_bb(self) -> List:
        return self.bb_storage_


    def return_nodes(self) ->List:
        return self.nodes_

