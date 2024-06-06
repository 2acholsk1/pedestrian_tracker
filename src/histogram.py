#!/usr/bin/env python3

import cv2
from pgmpy.factors.discrete import DiscreteFactor



class Histogram:

    def __init__(self, bound_box:list, new_obj_prob:float, factor_graph:DiscreteFactor) -> None:
        self.bound_box = bound_box
        self.new_obj_prob = new_obj_prob
        self.factor_graph = factor_graph


    def hist_bb_calc(self) -> list:
        h_range = [0, 180]
        s_range = [0, 256]
        gray_range = [0, 256]

        h_bins = 180
        s_bins = 256
        gray_bins = 256

        hist = []

        for iter, bound_box in enumerate(self.bound_box):

            bound_box = cv2.resize(bound_box, (500, 500))
            bound_box_hsv = cv2.cvtColor(bound_box, cv2.COLOR_BGR2HSV)
            bound_box_gray = cv2.cvtColor(bound_box, cv2.COLOR_BGR2GRAY)

            hist_h = cv2.calcHist(bound_box_hsv, [0], None, [h_bins], h_range, accumulate=False)
            cv2.normalize(hist_h, hist_h, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32FC1)
            hist_s = cv2.calcHist(bound_box_hsv, [1], None, [s_bins], s_range, accumulate=False)
            cv2.normalize(hist_s, hist_s, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32FC1)
            hist_gray = cv2.calcHist(bound_box_gray, [0], None, [gray_bins], gray_range, accumulate=False)
            cv2.normalize(hist_gray, hist_gray, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32FC1)

            hist.append([hist_h, hist_s, hist_gray])

        return hist

    def hist_bb_compare(self, bound_box_current_hist:list, bound_box_previous_hist:list) -> DiscreteFactor:

        for iter_curr, hist_cur in enumerate(bound_box_current_hist):
            similar_lst = []
            for iter_prev, hist_prev in enumerate(bound_box_previous_hist):
                hist_comp_h = cv2.compareHist(hist_prev[0], hist_cur[0], cv2.HISTCMP_CORREL)
                hist_comp_s = cv2.compareHist(hist_prev[1], hist_cur[1], cv2.HISTCMP_CORREL)
                hist_comp_gray = cv2.compareHist(hist_prev[2], hist_cur[2], cv2.HISTCMP_CORREL)

                similar = (hist_comp_h + hist_comp_s + hist_comp_gray)/3
                similar_lst.append(similar)

            factor = DiscreteFactor([str(iter_curr)], [len(bound_box_previous_hist) + 1], [[self.new_obj_prob ]+ similar_lst])
            self.factor_graph.add_factors(factor)
            self.factor_graph.add_edge(str(iter_curr),factor)

        return self.factor_graph


