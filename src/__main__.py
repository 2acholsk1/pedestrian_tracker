#!/usr/bin/env python3

import argparse
import os
from pathlib import Path



def compute_prob(images_path, bb_path):
    pass
    

    


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('data_dir', type=str)
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    images_dir = Path(os.path.join(str(data_dir), 'frames'))
    bb_dir = Path(os.path.join(str(data_dir), 'bboxes.txt'))
    
    images_path = sorted([img_path for img_path in images_dir.iterdir() if img_path.name.endswith('.jpg')])

    file = open(bb_dir, 'r')
    
    compute_prob()

