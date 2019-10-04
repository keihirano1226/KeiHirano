import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
import yaml
import tempfile
import argparse
import os
import numpy as np
import tf
import pandas as pd
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

def calc_regi_image(depth, ir_camera, color, color_camera, rot, trans):
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
    registered = np.zeros((424,512,3))
    for y_d in range(424):
        for x_d in range(512):
            if depth[y_d, x_d] != 0:
                x = (x_d - cx_d) * depth[y_d, x_d] / fx_d
                y = (y_d - cy_d) * depth[y_d, x_d] / fy_d
                z = depth[y_d, x_d]
                P3D = np.array([x,y,z])
                P3D2 = np.dot(rot , P3D) + trans
                x_color = int(round((P3D2[0] * fx_rgb / P3D2[2]) + cx_rgb))
                y_color = int(round((P3D2[1] * fy_rgb / P3D2[2]) + cy_rgb))

                if (x_color <= 512)  and (x_color >= 0) and (y_color <= 424) and (y_color >= 0):
                    registered[y_d, x_d] = color[y_color, x_color]

                #registered[y_d, x_d] = color[y_color, x_color]
            elif depth[y_d, x_d] == 0:
                    registered[y_d, x_d] = 0
    return registered, y_d, x_d

if __name__ == "__main__":
    pose_data = read_calib_pose("./cali_test/calib_pose.yaml")
    rot , trans= calc_rot_trans(pose_data)
    color_data = read_calib_pose("./cali_test/calib_color.yaml")
    ir_data = read_calib_pose("./cali_test/calib_ir.yaml")
    ir_camera , ir_dist = calc_proj_dist(ir_data)
    color_camera , color_dist = calc_proj_dist(color_data)
    """
    depth = cv2.imread("./images/0000000001.tiff", cv2.IMREAD_ANYDEPTH)
    color = cv2.imread("./images/0000000001.jpg")
    """
    depth = cv2.imread("/home/kei/document/experiments/BioEngen/MA330_2/depth/0000000001.png", cv2.IMREAD_ANYDEPTH)
    color = cv2.imread("/home/kei/document/experiments/BioEngen/MA330_2/color/0000000001.jpg")

    ir_h, ir_w = depth.shape[:2]
    color_h, color_w = color.shape[:2]
    trans2 = np.array(trans)
    print(type(trans2))
    print(color.shape)
    ir_newcameramtx, roi=cv2.getOptimalNewCameraMatrix(ir_camera,ir_dist,(ir_w,ir_h),1,(ir_w,ir_h))
    ir_undistorted = cv2.undistort(depth, ir_camera, ir_dist)
    cv2.imwrite("calitest.png",ir_undistorted)
    death = pd.DataFrame(ir_undistorted)
    death.to_csv("test.csv")
    cx_d = color_camera[0,2]
    cy_d = color_camera[1,2]
    fx_d = color_camera[0,0]
    fy_d = color_camera[1,1]
    print(cx_d)
    print(cy_d)
    print(fx_d)
    print(fy_d)
    registered_image, y_d1, xd_1 = calc_regi_image(ir_undistorted, ir_camera, color, color_camera, rot, trans2)
    cv2.imwrite("regitest2.jpg",registered_image)
    print(registered_image[0,0])
    print(y_d1)
