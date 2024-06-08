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
