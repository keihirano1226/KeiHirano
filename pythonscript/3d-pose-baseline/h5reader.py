# -*- coding: utf-8 -*-
from __future__ import division

import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import h5py
import glob
import copy

# Joints in H3.6M -- data has 32 joints, but only 17 that move; these are the indices.
H36M_NAMES = ['']*32
H36M_NAMES[0]  = 'Hip'
H36M_NAMES[1]  = 'RHip'
H36M_NAMES[2]  = 'RKnee'
H36M_NAMES[3]  = 'RFoot'
H36M_NAMES[6]  = 'LHip'
H36M_NAMES[7]  = 'LKnee'
H36M_NAMES[8]  = 'LFoot'
H36M_NAMES[12] = 'Spine'
H36M_NAMES[13] = 'Thorax'
H36M_NAMES[14] = 'Neck/Nose'
H36M_NAMES[15] = 'Head'
H36M_NAMES[17] = 'LShoulder'
H36M_NAMES[18] = 'LElbow'
H36M_NAMES[19] = 'LWrist'
H36M_NAMES[25] = 'RShoulder'
H36M_NAMES[26] = 'RElbow'
H36M_NAMES[27] = 'RWrist'


"""
  Loads 2d ground truth from disk, and puts it in an easy-to-acess dictionary

  Args
    bpath: String. Path where to load the data from
    subjects: List of integers. Subjects whose data will be loaded
    actions: List of strings. The actions to load
    dim: Integer={2,3}. Load 2 or 3-dimensional data
  Returns:
    data: Dictionary with keys k=(subject, action, seqname)
      values v=(nx(32*2) matrix of 2d ground truth)
      There will be 2 entries per subject/action if loading 3d data
      There will be 8 entries per subject/action if loading 2d data
"""
dim = 3
subjects = [1]
actions = ["Posing"]
if dim in [2,3]:

    data = {}

    for subj in subjects:
        for action in actions:

            print('Reading subject {0}, action {1}'.format(subj, action))
            dpath = './data/h36m/S1/MyPoses/3D_positions'
            fnames = glob.glob( dpath  + '*.h5')
            #print(fnames)
            loaded_seqs = 0
        for fname in fnames:
            seqname = os.path.basename( fname )

            # This rule makes sure SittingDown is not loaded when Sitting is requested
            if action == "Sitting" and seqname.startswith( "SittingDown" ):
                continue

            # This rule makes sure that WalkDog and WalkTogeter are not loaded when
            # Walking is requested.
            if seqname.startswith( action ):
                print( fname )
                loaded_seqs = loaded_seqs + 1

            with h5py.File( fname, 'r' ) as h5f:
                poses = h5f['{0}D_positions'.format(dim)][:]

                poses = poses.T
                data[ (subj, action, seqname) ] = poses
                print(type(data))
        if dim == 2:
            assert loaded_seqs == 8, "Expecting 8 sequences, found {0} instead".format( loaded_seqs )
        else:
            assert loaded_seqs == 2, "Expecting 2 sequences, found {0} instead".format( loaded_seqs )
print(data)
