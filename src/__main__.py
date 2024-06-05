#!/usr/bin/env python3

import os
import cv2
import argparse
import numpy as np
from pathlib import Path
from pgmpy.models import FactorGraph
from boundbox import BoundBox
from histogram import Histogram


def compute_prob(images_path, bb_file):

    hist_curr = []
    hist_prev = []
    bb_none = False

    prob_new = 0.3
    
    for img_num in range(len(images_path)):
        
        nodes = []
        coordinates_bb = []
        factor_graph = FactorGraph()

        text = bb_file.readline().rstrip("\n")
        bb_num = bb_file.readline().rstrip("\n")

        img = cv2.imread(str(images_path[img_num]), cv2.IMREAD_UNCHANGED)
        # cv2.imshow("tyk", img)
        # cv2.waitKey(0)

        hist_prev = hist_curr


        if bb_num == '0':
            print('')
            bb_none = True
            continue
        
        hist_curr = []
        bb_curr = []
        
        for _ in range(int(float(bb_num))):
            coordinates_bb.append(bb_file.readline().rstrip("\n").split(" "))

        bb = BoundBox(img, coordinates_bb)
        bb.compute_bb()

        bb_curr = bb.return_bb()
        nodes = bb.return_nodes()

        factor_graph.add_nodes_from(nodes)

        hist = Histogram(bb_curr, prob_new, factor_graph)
        hist_curr = hist.hist_bb_calc()

        if bb_none:
            bb_none = False
            for _ in range(int(float(bb_num))):
                print("-1", end=" ")
            continue

        matrix_size = int(float(len(hist_prev))) + 1
        nodes_matrix_possibility = np.ones((matrix_size, matrix_size))

        nodes_matrix_possibility = [[0 if row == column else nodes_matrix_possibility[row][column] for row in range(matrix_size)] for column in range(matrix_size)]
        nodes_matrix_possibility[0][0] = 1

        # if hist_prev != 0:


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('data_dir', type=str)
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    images_dir = Path(os.path.join(str(data_dir), 'frames'))
    bb_dir = Path(os.path.join(str(data_dir), 'bboxes.txt'))
    
    images_path = sorted([img_path for img_path in images_dir.iterdir() if img_path.name.endswith('.jpg')])

    file = open(bb_dir, 'r')
    
    compute_prob(images_path, file)

