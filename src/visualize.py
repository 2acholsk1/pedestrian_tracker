#!/usr/bin/env python3

import cv2
import os
import argparse
from pathlib import Path

class Visualizer:
    def __init__(self, images_path, results_path, bb_file_path, frames_dir):
        self.images_path = images_path
        self.results_path = results_path
        self.bb_file_path = bb_file_path
        self.frames_dir = frames_dir

    def load_results(self):
        with open(self.results_path, 'r') as file:
            self.results = [list(map(int, line.strip().split())) for line in file.readlines()]

    def load_bb(self):
        with open(self.bb_file_path, 'r') as file:
            self.bb = []
            while True:
                img_name = file.readline().strip()
                if not img_name:
                    break
                num_boxes = int(file.readline().strip())
                boxes = []
                for _ in range(num_boxes):
                    boxes.append(list(map(float, file.readline().strip().split())))
                self.bb.append(boxes)

    def draw_bb(self, image, boxes, results):
        for i, coords in enumerate(boxes):
            x, y, w, h = map(int, coords)
            color = (0, 255, 0)
            if results[i] == -1:
                color = (0, 0, 255)
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            cv2.putText(image, str(results[i]), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        return image

    def visualize(self):
        if not self.images_path:
            raise ValueError("No images found in the specified directory.")

        if not os.path.exists(self.frames_dir):
            os.makedirs(self.frames_dir)

        for idx, (img_path, boxes, results) in enumerate(zip(self.images_path, self.bb, self.results)):
            img = cv2.imread(str(img_path), cv2.IMREAD_UNCHANGED)
            if img is None:
                print(f"Warning: Image at {img_path} could not be read.")
                continue
            img_with_bboxes = self.draw_bb(img, boxes, results)
            cv2.imwrite(os.path.join(self.frames_dir, f"frame_{idx:03d}.jpg"), img_with_bboxes)

        print(f"Frames saved as images in {self.frames_dir}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('data_dir', type=str)
    parser.add_argument('result', type=str)
    parser.add_argument('frames_dir', type=str)
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    result_dir = Path(args.result)
    frames_dir = Path(args.frames_dir)
    images_dir = Path(os.path.join(str(data_dir), 'frames'))
    bb_file_path = Path(os.path.join(data_dir, 'bboxes.txt'))
    results_path = Path(os.path.join(str(result_dir), 'results.txt'))

    images_path = sorted([img_path for img_path in images_dir.iterdir() if img_path.name.endswith('.jpg')])

    if not images_path:
        print("No images found in the specified directory. Please check the path and try again.")
        exit(1)

    visualizer = Visualizer(images_path, results_path, bb_file_path, frames_dir)
    visualizer.load_results()
    visualizer.load_bb()
    visualizer.visualize()
