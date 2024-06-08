#!/usr/bin/env python3

import cv2
from pgmpy.factors.discrete import DiscreteFactor
from typing import List


class Histogram:

    def __init__(self, bb:List, new_obj_prob:float, factor_graph:DiscreteFactor) -> None:
        self.bb_ = bb
        self.new_obj_prob_ = new_obj_prob
        self.factor_graph_ = factor_graph


    def hist_bb_calc(self) -> List:
        h_range = [0, 180]
        s_range = [0, 256]
        g_range = [0, 256]

        h_bins = 180
        s_bins = 256
        g_bins = 256

        hist = []

        for iter, bb in enumerate(self.bb_):

            bb = cv2.resize(bb, (500, 500))
            bb_hsv = cv2.cvtColor(bb, cv2.COLOR_BGR2HSV)
            bb_gray = cv2.cvtColor(bb, cv2.COLOR_BGR2GRAY)

            hist_h = cv2.calcHist([bb_hsv], [0], None, [h_bins], h_range, accumulate=False)
            cv2.normalize(hist_h, hist_h, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32FC1)
            hist_s = cv2.calcHist([bb_hsv], [1], None, [s_bins], s_range, accumulate=False)
            cv2.normalize(hist_s, hist_s, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32FC1)
            hist_g = cv2.calcHist([bb_gray], [0], None, [g_bins], g_range, accumulate=False)
            cv2.normalize(hist_g, hist_g, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32FC1)

            hist.append([hist_h, hist_s, hist_g])

        return hist

    def hist_bb_compare(self, bb_current_hist:List, bb_previous_hist:List) -> DiscreteFactor:

        for iter_curr, hist_cur in enumerate(bb_current_hist):
            similar_lst = []
            for iter_prev, hist_prev in enumerate(bb_previous_hist):
                hist_comp_h = cv2.compareHist(hist_prev[0], hist_cur[0], cv2.HISTCMP_CORREL)
                hist_comp_s = cv2.compareHist(hist_prev[1], hist_cur[1], cv2.HISTCMP_CORREL)
                hist_comp_g= cv2.compareHist(hist_prev[2], hist_cur[2], cv2.HISTCMP_CORREL)

                similar = (hist_comp_h + hist_comp_s + hist_comp_g)/3
                if similar <= 0.0:
                    similar = 0.01
                similar_lst.append(similar)

            factor = DiscreteFactor([str(iter_curr)], [len(bb_previous_hist) + 1], [[self.new_obj_prob_] + similar_lst])
            self.factor_graph_.add_factors(factor)
            self.factor_graph_.add_edge(str(iter_curr),factor)

        return self.factor_graph_


