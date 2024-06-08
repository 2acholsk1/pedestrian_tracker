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


    # def _parse_file(self):
    #     data = {}
    #     with open(self.file_path, 'r') as file:
    #         lines = file.readlines()
    #         i = 0
    #         while i < len(lines):
    #             line = lines[i].strip()
    #             if line.endswith('.jpg'):
    #                 current_image = line
    #                 data[current_image] = []
    #                 i += 1
    #                 box_count = int(lines[i].strip())
    #                 i += 1
    #                 for _ in range(box_count):
    #                     coords = List(map(float, lines[i].strip().split()))
    #                     data[current_image].append(coords)
    #                     i += 1
    #             else:
    #                 i += 1
    #     return data

    # def get_bounding_boxes(self, image_name):
    #     return self.data.get(image_name, [])
    
    def return_bb(self) -> List:
        return self.bb_storage_

    def return_nodes(self) ->List:
        return self.nodes_

# Usage
# bbox = BoundBox('data/c6s1/bboxes.txt')
# print(bbox.get_bounding_boxes('c6s1_002576.jpg'))
