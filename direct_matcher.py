import sqlite3
import numpy as np
import pdb
import sys
import cv2
import scipy.io as sio
import os
import math

def get_good_matches(matches): #Lowe's ratio test
    good = []
    for m,n in matches:
        if m.distance < 0.7 * n.distance: # or 0.75
            good.append([m])
    return good

def direct_matching(query_keypoints_xy_descriptors):

    query_descriptors = query_keypoints_xy_descriptors[:,2:130]

    train_descriptors_direct_match = np.loadtxt('direct_matching_results/averages_3Dpoints_xyz.txt')
    train_descriptors_direct_match = train_descriptors_direct_match.astype(np.float32)

    print "matching.. direct.."

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(query_descriptors, train_descriptors_direct_match[:,0:128], k=2)

    good = get_good_matches(matches)

    print "found this many good matches direct: " + str(np.shape(good)[0])

    final_match_array_direct = np.empty((0, 5))
    for good_match in good:
        queryIndex = good_match[0].queryIdx
        trainIndex = good_match[0].trainIdx
        final_match_array_row = np.concatenate((query_keypoints_xy_descriptors[queryIndex,0:2], train_descriptors_direct_match[trainIndex,129:132]) , axis = 0)
        final_match_array_direct = np.concatenate((final_match_array_direct, final_match_array_row.reshape([1,5])), axis = 0)

    return final_match_array_direct, np.shape(good)[0]

# # ..or FLANN
# FLANN_INDEX_KDTREE = 0
# index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
# search_params = dict(checks=50)   # or pass empty dictionary
# flann = cv2.FlannBasedMatcher(index_params,search_params)
#
# train_descriptors = train_descriptors.astype(np.float32) # minor formatting fix
# query_descriptors = np.ascontiguousarray(query_descriptors)
# train_descriptors = np.ascontiguousarray(train_descriptors)
#
# matches = flann.knnMatch(query_descriptors, train_descriptors, k=2)
