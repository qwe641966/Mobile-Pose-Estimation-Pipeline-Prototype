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

def image_retrieval_matching(query_keypoints_xy_descriptors, data_dir, similar_images_names):

    print "loading correspondences.."
    correspondences = np.empty((0, 133))
    for similar_image in similar_images_names:
        similar_image_text_file = data_dir+"/points_correspondences/"+similar_image.split("\n")[0]+"/correspondences.txt"
        array = np.loadtxt(similar_image_text_file)
        correspondences = np.concatenate((correspondences, array), axis = 0)

    print "matching.. image retrieval.."
    query_descriptors = query_keypoints_xy_descriptors[:,2:130]
    train_descriptors = correspondences[:,0:128]
    train_descriptors = train_descriptors.astype(np.float32) # minor formatting fix

    bf = cv2.BFMatcher()

    matches = bf.knnMatch(query_descriptors, train_descriptors, k=2)

    good = get_good_matches(matches)

    print "found this many good matches: " + str(np.shape(good)[0])

    final_match_array = np.empty((0, 5))
    for good_match in good:
        queryIndex = good_match[0].queryIdx
        trainIndex = good_match[0].trainIdx
        final_match_array_row = np.concatenate((query_keypoints_xy_descriptors[queryIndex,0:2], correspondences[trainIndex,130:133]) , axis = 0)
        final_match_array = np.concatenate((final_match_array, final_match_array_row.reshape([1,5])), axis = 0)


    return final_match_array, np.shape(good)[0]

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
