#!/usr/bin/env python3

import os
import argparse
from pathlib import Path

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
    parser.add_argument('ground_truth_file', type=str)
    args = parser.parse_args()

    ground_truth_file = args.ground_truth_file
    converted_ground_truth_file = "data/check/converted_ground_truth.txt"
    convert_ground_truth(ground_truth_file, converted_ground_truth_file)

    predictions_file = "data/check/results.txt"
    evaluate_accuracy(converted_ground_truth_file, predictions_file)
