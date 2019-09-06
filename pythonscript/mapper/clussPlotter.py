import chart_studio.plotly as py
import plotly.graph_objs as go
import datetime
import pandas as pd
import numpy as np
import plotly.offline as offline
from joint_vector import JointVector
from body_columns import MainJointAngleList, joint2coordinate

csvpass1 = "/home/kei/document/experiments/method/1,3_result/AveragePose1.csv"
csvpass2 = "/home/kei/document/experiments/method/1,3_result/AveragePose2.csv"
posedf1 = pd.read_csv(csvpass1, index_col = 0)
posedf2 = pd.read_csv(csvpass2, index_col = 0)
clusterlist = [posedf1, posedf2]
data = []
body = posedf1[bodycolumns].values
for i in range(len(OpenPoseJoint)):

    xs = body[:,3*i]
    ys = body[:,3*i+1]
    zs = body[:,3*i+2]
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

layout = go.Layout(
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=0
    ),
    # xyz軸のスケールを統一
    scene=dict(aspectmode='cube'),
    showlegend=False,
)
fig = go.Figure(data=data, layout=layout)
offline.plot(fig, filename='cluster.html')
