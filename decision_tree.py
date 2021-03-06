# -*- coding: utf-8 -*-
"""Decision Tree

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UmVNEaHnUfsGpkB5e-WMFPcnNNaoors9
"""

# from google.colab import drive
# drive.mount('/content/drive/')

import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd

# data = np.load('/content/drive/My Drive/Colab Notebooks/Training Data Testing/testingdata.npy')

#calculating the purity of data set using gini impurity entropy requires more computation and data set is large
def calc_gini_index(data):
    if len(data) > 0:
        _, freq = np.unique(data[:, 81], return_counts = True)
        if freq.shape == (2,):
            neg, pos =  freq
        else:
            neg, pos = freq, 0
        rows_ = len(data[:, 81])
        prob_pos = pos / rows_
        prob_neg = neg / rows_
        gini_index = 1 - (prob_pos**2 + prob_neg**2)
        return gini_index
    else: 
        gini_index = 0
        return gini_index

#calculates the information gain after the split is made using gini impurity
def information_gain(parent_data, spltL, spltR):
    gini_spltL = calc_gini_index(spltL)
    gini_spltR = calc_gini_index(spltR)
    info_gain = (calc_gini_index(parent_data) - (calc_gini_index(spltL) * (len(spltL[:, 81])/len(parent_data[:, 81]))+\
                                                 calc_gini_index(spltR) * (len(spltR[:, 81])/len(parent_data[:, 81]))))
    return info_gain

#getting all the possible splits a node can  make, not evaluating the information gain of making each split
def get_possible_splits(data):

    pos_splts = {}

    for i in range(len(data.T)-1):
        splt_vals = np.empty([1,])

        for e in range(16):
            splt_val = np.array([15 * e])
            splt_vals = np.concatenate((splt_vals, splt_val))

        splt_vals = tuple(splt_vals[1:])
        possible_splts = {i: splt_vals}
        pos_splts.update(possible_splts)

    return pos_splts

#classifying data after node has required purity
def classify_end_data(data):
    label_col = data[:, 81]
    label, label_counts = np.unique(label_col, return_counts = True)
    ind = label_counts.argmax()
    classification = label[ind] 
    return classification

def check_purity(data):
    purity = calc_gini_index(data)
    if purity < 0.00001:
        label = classify_end_data(data)

def split_data(data, split_val, col):

    splitL = np.empty([82,])
    splitR = np.empty([82,])

    for i in range(len(data)):
        if data[i, col] <= split_val:
            splitL = np.concatenate((splitL, data[i, :]))
        elif data[i, col] > split_val:
            splitR = np.concatenate((splitR, data[i, :]))
    splitL = splitL[82:]
    splitR = splitR[82:]
    colindL = len(splitL) // 82
    colindR = len(splitR) //82
    if splitL.shape[0] > 0:
        splitL = splitL.reshape([colindL, 82])
    if splitR.shape[0] > 0:
        splitR = splitR.reshape([colindR, 82])
    return splitL, splitR

def find_best_split(data):
    best_info_gain = 0
    split_value = 0
    pos_splits = get_possible_splits(data)
    for i in range(len(data.T)-1):
        for e in range(16):
            split_val = pos_splits[i][e]
            splitL, splitR = split_data(data, split_val, i)
            if len(splitL) > 0 and len(splitR) > 0:
                info_gain = information_gain(data, splitL, splitR)
                if info_gain > best_info_gain:
                    best_info_gain = info_gain
                    col = i
                    fin_split_val = split_val
                    spltLfin = splitL
                    spltRfin = splitR
    

    return col, fin_split_val, spltLfin, spltRfin


col, fin_split_val, _, _ = find_best_split(data)
print(col)
print(fin_split_val)

#uses dictionaries within dictonary to represent the decision tree

def grow_tree(data):
    print("---------------")
    print(len(data))
    print(calc_gini_index(data))
    print(np.count_nonzero(data[:, 81] > 0))
    purity = calc_gini_index(data)

    if purity < 0.05:
        classification = classify_end_data(data)
        print(classification)
        return classification

    else:
        col, fin_split_val, splitLfin, splitRfin = find_best_split(data)
        splitL, splitR = split_data(data, fin_split_val, col)
        question = "{} <= {}".format(col, fin_split_val)
        sub_tree = {question:[]}

        splitLQ, splitRQ = grow_tree(splitL), grow_tree(splitR)

        sub_tree[question].append(splitLQ)
        sub_tree[question].append(splitRQ)
        return sub_tree

y = grow_tree(data)
print(y)

# f = open("/content/drive/My Drive/Colab Notebooks/Training Data Testing/tree.txt", "w")
# f.write(str(y))
# f.close()

