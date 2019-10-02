import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
import yaml
import tempfile
import argparse
import os
import numpy as np
import tf
def read_calib_pose(fname):
    tmp = tempfile.TemporaryFile()
    # we need modify original yaml file because yaml.load(fname) simply will fail

    with open(fname, "r") as f:
        reader = f.readlines()
        for row in reader:
            if row[0] == "%":
                # remove first line: "%YAML:1.0"
                continue
            if row.find("!!") != -1:
                # remove "!!opencv-matrix"
                row = row[:row.find("!!")] + os.linesep
            row2 = row.encode("utf-8")
            tmp.write(row2)
    tmp.seek(0)
    data = yaml.load(tmp)
    return data

def calc_rot_trans(data):
    rot = np.resize(data["rotation"]["data"], (3, 3))
    trans = data["translation"]["data"]
    #rpy = tf.transformations.euler_from_matrix(mat)
    return rot,trans

def calc_proj_dist(data):
    camera = np.resize(data["cameraMatrix"]["data"], (3, 3))
    dist = np.resize(data["distortionCoefficients"]["data"], (5))
    #rpy = tf.transformations.euler_from_matrix(mat)
    return camera,dist

def calc_regi_image(depth, ir_camera, color, color_camera):
    x_d = 0
    y_d = 0
    cx_d = ir_camera[0,2]
    cy_d = ir_camera[1,2]
    fx_d = ir_camera[0,0]
    fy_d = ir_camera[1,1]
    cx_rgb = color_camera[0,2]
    cy_rgb = color_camera[1,2]
    fx_rgb = color_camera[0,0]
    fy_rgb = color_camera[1,1]
    ir_h, ir_w = depth.shape[:2]
    for y_d in range(ir_h):
        for x_d in range(ir_w):
            P3D = np.array([])

if __name__ == "__main__":
    pose_data = read_calib_pose("./cali_test/calib_pose.yaml")
    rot , trans= calc_rot_trans(pose_data)
    color_data = read_calib_pose("./cali_test/calib_color.yaml")
    ir_data = read_calib_pose("./cali_test/calib_ir.yaml")
    ir_camera , ir_dist = calc_proj_dist(ir_data)
    color_camera , color_dist = calc_proj_dist(color_data)
    depth = cv2.imread("./images/0000000001.tiff", cv2.IMREAD_ANYDEPTH)
    color = cv2.imread("./images/0000000001.jpg")
    ir_h, ir_w = depth.shape[:2]
    color_h, color_w = color.shape[:2]
    print(ir_dist)
    """
    ir_newcameramtx, roi=cv2.getOptimalNewCameraMatrix(ir_camera,ir_dist,(ir_w,ir_h),1,(ir_w,ir_h))
    ir_undistorted = cv2.undistort(depth, ir_camera, ir_dist)
    color_newcameramtx, roi=cv2.getOptimalNewCameraMatrix(color_camera,color_dist,(color_w,color_h),1,(color_w,color_h))
    color_undistorted = cv2.undistort(color, color_camera, color_dist)
    cv2.imwrite("calitest.png",ir_undistorted)
    cv2.imwrite("calitest2.jpg",color_undistorted)
    """
