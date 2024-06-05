#!/usr/bin/env python3

import cv2
class BoundBox:

    def __init__(self, image: cv2.Mat, coordinates: list):
        self.coordinates = coordinates
        self.img = image
        self.nodes = []
        self.bb_storage = []

    def compute_coords(self, coordinates: list) -> None:
        self.x = int(float(coordinates[0]))
        self.y = int(float(coordinates[1]))
        self.w = int(float(coordinates[2]))
        self.h = int(float(coordinates[3]))

    
    def compute_bb(self) -> None:
        for iter, coords in enumerate(self.coordinates):
            self.nodes.append(str(iter))
            self.compute_coords(coords)
            self.bb_storage.append(self.img[self.x + int(self.h/4) : self.x + int(3*self.h/4),
                                            self.y + int(self.w/4) : self.y + int(3*self.w/4)])


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
    #                     coords = list(map(float, lines[i].strip().split()))
    #                     data[current_image].append(coords)
    #                     i += 1
    #             else:
    #                 i += 1
    #     return data

    # def get_bounding_boxes(self, image_name):
    #     return self.data.get(image_name, [])
    
    def return_bb(self) -> list:
        return self.bb_storage

    def return_nodes(self) ->list:
        return self.nodes

# Usage
bbox = BoundBox('data/c6s1/bboxes.txt')
print(bbox.get_bounding_boxes('c6s1_002576.jpg'))
