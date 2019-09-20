import chart_studio.plotly as py
import plotly.graph_objs as go
import datetime
import pandas as pd
import numpy as np
import plotly.offline as offline
from joint_vector import JointVector
from body_columns import MainJointAngleList, joint2coordinate, bodycolumns

csvpass1 = "/home/kei/document/experiments/BioEngen/ana/result/AveragePose1.csv"
csvpass2 = "/home/kei/document/experiments/BioEngen/ana/result/AveragePose2.csv"
csvpass3 = "/home/kei/document/experiments/BioEngen/ana/product_points.csv"
posedf1 = pd.read_csv(csvpass1, index_col = 0)
posedf2 = pd.read_csv(csvpass2, index_col = 0)
productdf = pd.read_csv(csvpass3)
clusterlist = [posedf1, posedf2]
data = []
#body = posedf1[bodycolumns].values
body1 = posedf1.loc[:,["MidHipX","MidHipY","MidHipZ"]].values
#body1 = posedf1.values
#body2 = posedf2.values
body2 = posedf2.loc[:,["MidHipX","MidHipY","MidHipZ"]].values

product = productdf.values
for i in range(1):

    xs = body1[:,3*i]
    ys = body1[:,3*i+1]
    zs = body1[:,3*i+2]
    data.append(go.Scatter3d(
            x=xs,
            y=ys,
            z=zs,
            mode='markers',
            marker=dict(
                color='rgb(100,100,200)',
                size=2,
                opacity=0.8
            )
        ))
for i in range(1):

    xs = body2[:,3*i]
    ys = body2[:,3*i+1]
    zs = body2[:,3*i+2]
    data.append(go.Scatter3d(
            x=xs,
            y=ys,
            z=zs,
            mode='markers',
            marker=dict(
                color='rgb(200,140,100)',
                size=2,
                opacity=0.8
            )
        ))

cube1 = go.Mesh3d(
    x = [0,0,0.44,0.44,0,0,0.44,0.44],
    y = [-0.18,0.586,-0.18,0.586,-0.18,0.586,-0.18,0.586],
    z = [0,0,0,0,-0.44,-0.44,-0.44,-0.44],
    i=[0,1,1,1,1,3,0,2,4,5,2,3],
    j=[1,3,0,4,3,7,2,6,5,6,3,7],
    k=[2,2,4,5,5,5,4,4,6,7,6,6],
    opacity=1,
    color='cyan'
    )
data.append(cube1)
cube2 = go.Mesh3d(
    x = [0.44,0.44,0.83,0.83,0.44,0.44,0.83,0.83],
    y = [-0.17,-0.15,-0.17,-0.15,-0.17,-0.15,-0.17,-0.15],
    z = [0.31,0.31,0.31,0.31,0,0,0,0],
    i=[0,1,1,1,1,3,0,2,4,5,2,3],
    j=[1,3,0,4,3,7,2,6,5,6,3,7],
    k=[2,2,4,5,5,5,4,4,6,7,6,6],
    opacity=1,
    color='cyan'
    )
data.append(cube2)
layout = go.Layout(
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=0
    ),
    # xyz軸のスケールを統一
)
fig = go.Figure(data=data, layout=layout)
offline.plot(fig, filename='/home/kei/document/experiments/BioEngen/ana/result/MidHip.html',auto_open=False)
