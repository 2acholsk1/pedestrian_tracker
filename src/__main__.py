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


def compute_prob(images_path_arg, bb_file_arg):

    images_path = images_path_arg
    bb_file = bb_file_arg

    hist_curr = []
    hist_prev = []
    bb_curr = []

    bb_none = 0

    prob_new = 0.3
    
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
            for _ in range(int(float(bb_num))):
                print("-1", end=" ")
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
            print(*([v - 1 for v in val]), sep=" ")
            

            with open ("main_out.txt", "a") as file:
                file.write(" ".join(map(str, [v - 1 for v in val])) + "\n")


def convert_ground_truth(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        while True:
            image_id = infile.readline().strip()
            if not image_id:
                break
            person_count = int(infile.readline().strip())
            results = []
            for _ in range(person_count):
                line = infile.readline().strip().split()
                results.append(int(line[0]))
            outfile.write(" ".join(map(str, results)) + "\n")
    print(f"Converted ground truth saved to {output_file}")

def evaluate_accuracy(ground_truth_file, predictions_file):
    correct = 0
    total = 0

    with open(ground_truth_file, 'r') as gt_file, open(predictions_file, 'r') as pred_file:
        for gt_line, pred_line in zip(gt_file, pred_file):
            gt_parts = gt_line.strip().split()
            pred_parts = pred_line.strip().split()

            if len(gt_parts) != len(pred_parts):
                print(f"Error: Mismatch in number of predictions for line {gt_line}")
                continue

            correct += sum(1 for gt, pred in zip(gt_parts, pred_parts) if gt == pred)
            total += len(gt_parts)

    if total == 0:
        print("Error: No data to evaluate. Check the input files.")
        return

    accuracy = correct / total

    print(f"Accuracy: {accuracy:.2f} ({correct} correct out of {total} total)")



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('data_dir', type=str)
    parser.add_argument('ground_truth_file', type=str)
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    images_dir = Path(os.path.join(str(data_dir), 'frames'))
    bb_dir = Path(os.path.join(data_dir, 'bboxes.txt'))
    
    images_path = sorted([img_path for img_path in images_dir.iterdir() if img_path.name.endswith('.jpg')])

    file = open(bb_dir, 'r')
    
    compute_prob(images_path, file)

    ground_truth_file = args.ground_truth_file
    converted_ground_truth_file = "converted_ground_truth.txt"
    convert_ground_truth(ground_truth_file, converted_ground_truth_file)

    predictions_file = "main_out.txt"
    evaluate_accuracy(converted_ground_truth_file, predictions_file)

