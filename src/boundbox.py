#!/usr/bin/env python3

class BoundBox:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self._parse_file()

    def _parse_file(self):
        data = {}
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                if line.endswith('.jpg'):
                    current_image = line
                    data[current_image] = []
                    i += 1
                    box_count = int(lines[i].strip())
                    i += 1
                    for _ in range(box_count):
                        coords = list(map(float, lines[i].strip().split()))
                        data[current_image].append(coords)
                        i += 1
                else:
                    i += 1
        return data

    def get_bounding_boxes(self, image_name):
        return self.data.get(image_name, [])

# Usage
bbox = BoundBox('data/c6s1/bboxes.txt')
print(bbox.get_bounding_boxes('c6s1_002576.jpg'))
