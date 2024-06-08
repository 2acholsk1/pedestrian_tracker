# PEDESTRIAN TRACKER

## Table of Contents
- [Main goal](#main-goal)
- [Installation](#installation)
- [Usage](#usage)
- [Results](#results)
- [Documentation](#documentation)


## Main goal

A pedestrian tracking system using probabilistic graph models to assign bounding rectangles (Bounding Boxes) to people in consecutive video frames

## Installation

Clone repository:
```bash
git clone https://github.com/2acholsk1/pedestrian_tracker.git
cd pedestrian_tracker
```

After clone repository, you need to setup virtual environemnt, with which commands in the Makefile will help:
```bash
make setup-venv
```
Remember to activate venv with command: `source bin/activate`.

Then, you can easily build and install package by using:
```bash
make setup
```


## Usage

To start the program type, remeber to add path which contain frames of video to analyze:
```bash
python3 src/__main__.py path/to/frames/folder
```

If you want to ocheck accuracy, remember to add path to file with correct answers:
```bash
python3 src/result_accuracy.py path/to/file
```


## Results

Overall accuracy for c6s1 data folder is **95%, 2585 correct answers out of 2733 total**.
![pedestrians gif](data/pedestrians.gif)

## Documentation
The project consists of two main classes BoundBox and Histogram. 

BoundBox class manages rectangular regions (bounding boxes) on images.
Methods:
- __init(self, coordinates: list, image: cv2.Mat)__: Initializes with bounding box coordinates and an image.
- __compute_coords(self, coordinates: list)__: Converts and stores coordinates.
- __compute_bb(self)__: Computes and extracts bounding boxes from the image.
- __return_bb(self) -> list__: Returns the list of bounding boxes.
- __return_nodes(self) -> list__: Returns the list of node identifiers.

Histogram class computes and compares histograms of bounding boxes.
Methods:
- __init(self, bb: list, new_obj_prob: float, factor_graph: DiscreteFactor)__: Initializes with bounding boxes, new object probability, and a factor graph.
- __hist_bb_calc(self) -> list__: Computes histograms for each bounding box.
- __hist_bb_compare(self, bb_current_hist: list, bb_previous_hist: list) -> DiscreteFactor__: Compares histograms between frames and updates the factor graph.

There is also an auxiliary class - Visualize, which, as the name suggest, is used to visualize effects of the project.

Main function processes the images and bounding boxes, computes histograms, compares them, and performs belief propagation to track or identify objects across frames.
## Code workflow
1. __Initialization__:
- Initialize variables for current and previous histograms (__hist_curr__, __hist_prev__), current bounding boxes (__bb_curr__), and a flag (__bb_none__) to handle cases with no bounding boxes.
- Set a probability for new objects (__prob_new__).
- Prepare a list to store results.
2. __Iterate Over Images__:
- Loop through each image in the provided image paths.
- For each image, read and discard the first line (usually the image filename).
3. __Read Bounding Box Information__:
- Read the number of bounding boxes (__bb_num__) for the current image.
- If no bounding boxes are present (__bb_num__ is "0"), set the bb_none flag and skip further processing for the current image.
4. __Compute Bounding Boxes__:
- If bounding boxes are present, create an instance of __BoundBox__ with the coordinates and image.
- Call __compute_bb__ method to extract bounding boxes.
- Retrieve the bounding boxes (__bb_curr__) and node identifiers (__nodes__).
- Add nodes to the factor graph.
5. __Compute Histograms__:
- Create an instance of __Histogram__ with the current bounding boxes, new object probability, and factor graph.
- Call __hist_bb_calc__ method to compute histograms for the current bounding boxes.
6. __Handle No Bounding Boxes in Previous Image__:
- If __bb_none__ flag is set (no bounding boxes in the previous image), reset the flag, append __-1__ results for the current image, and skip further processing.
7. __Setup Node Possibility Matrix__:
- Create a matrix to represent the possibilities of node connections.
- Initialize the matrix with ones and set diagonal elements to zero (to prevent self-connections).
8. __Compare Histograms and Update Factor Graph__:
- If previous histograms are available, call __hist_bb_compare__ method to compare current and previous histograms, and update the factor graph.
- Use combinations of current and previous histogram indices to create and add factors to the factor graph.
- Add edges to the factor graph based on histogram comparisons.
9. __Perform Belief Propagation__:
- Create an instance of __BeliefPropagation__ with the factor graph.
- Calibrate the factor graph using the __calibrate__ method.
- Query the factor graph to determine the most probable states of the variables (bounding boxes).
- Store and print the results, adjusting the indices as needed.
10. __Handle No Previous Histograms__:
- If no previous histograms are available, append __-1__ results for the current image.
11. __Write Results to File__:
- After processing all images, write the results to a text file ('data/check/results.txt').

