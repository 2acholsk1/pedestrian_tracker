#!/usr/bin/env python3

import os
import cv2
import argparse
import numpy as np
from pathlib import Path
from pgmpy.models import FactorGraph
from pgmpy.factors.discrete import DiscreteFactor
from pgmpy.inference import BeliefPropagation
from itertools import combinations
from boundbox import BoundBox
from histogram import Histogram

def main(images_path_arg, bb_file_arg):

    images_path = images_path_arg
    bb_file = bb_file_arg

    hist_curr = []
    hist_prev = []
    bb_curr = []

    bb_none = 0

    prob_new = 0.3
    
    results = []

    for img_num in range(len(images_path)):
        
        nodes = []
        coordinates_bb = []
        factor_graph = FactorGraph()

        _ = bb_file.readline().rstrip("\n")

        img = cv2.imread(str(images_path_arg[img_num]), cv2.IMREAD_UNCHANGED)

        bb_num = bb_file.readline().rstrip("\n")

        hist_prev = hist_curr

        if bb_num == "0":
            print('')
            bb_none = 1
            continue
        
        hist_curr = []
        bb_curr = []
        
        for _ in range(int(float(bb_num))):
            coordinates_bb.append(bb_file.readline().rstrip("\n").split(" "))

        bb = BoundBox(coordinates_bb, img)
        bb.compute_bb()

        bb_curr = bb.return_bb()
        nodes = bb.return_nodes()

        factor_graph.add_nodes_from(nodes)

        hist = Histogram(bb_curr, prob_new, factor_graph)
        hist_curr = hist.hist_bb_calc()

        if bb_none == 1:
            bb_none = 0
            results.append([-1 for _ in range(int(float(bb_num)))])
            continue

        matrix_size = int(float(len(hist_prev))) + 1
        nodes_matrix_possibility = np.ones((matrix_size, matrix_size))

        nodes_matrix_possibility = [[0 if row == column else nodes_matrix_possibility[row][column] for row in range(matrix_size)] for column in range(matrix_size)]
        nodes_matrix_possibility[0][0] = 1

        if hist_prev != 0:
            factor_graph = hist.hist_bb_compare(hist_curr, hist_prev)

            for h_curr, h_prev in combinations(range(int(bb_num)), 2):
                
                factor = DiscreteFactor([str(h_curr), str(h_prev)], [matrix_size, matrix_size], nodes_matrix_possibility)

                factor_graph.add_factors(factor)
                factor_graph.add_edge(str(h_curr), factor)
                factor_graph.add_edge(str(h_prev), factor)

            belief_propagation = BeliefPropagation(factor_graph)
            belief_propagation.calibrate()

            bp_results = (belief_propagation.map_query(factor_graph.get_variable_nodes()))

            keys = sorted(bp_results.keys())
            val = [bp_results[key] for key in keys]
            results.append([v - 1 for v in val])
            print(*([v - 1 for v in val]), sep=" ")
        else:
            results.append([-1 for _ in range(int(float(bb_num)))])
            print(*([-1 for _ in range(int(float(bb_num)))]), sep=" ")

    with open ("data/check/results.txt", "w") as file:
        for result in results:
            file.write(" ".join(map(str, result)) + "\n")

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('data_dir', type=str)
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    images_dir = Path(os.path.join(str(data_dir), 'frames'))
    bb_dir = Path(os.path.join(data_dir, 'bboxes.txt'))
    
    images_path = sorted([img_path for img_path in images_dir.iterdir() if img_path.name.endswith('.jpg')])

    file = open(bb_dir, 'r')
    
    main(images_path, file)
