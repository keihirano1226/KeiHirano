import plotly
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
plotly.tools.set_credentials_file(username='KeiHirano', api_key='krRfYzDQXbS3sZcZcpAf')
import numpy as np

df = pd.read_csv("/home/kei/document/experiments/2019.06.25/data2/3dboneRotated.csv")
print(df)
body = df.drop("Frame", axis = 1)
OpenPosecolumns = []
OpenPoseJoint = ["Neck","RSholder","LSholder","RElbow","LElbow","RWrist","LWrist","MidHip",\
"RHip","LHip","RKnee","LKnee","RAnkle","LAnkle"]
Coordinate2 = ["X","Y","Z"]
for point in OpenPoseJoint:
    for coordinate in Coordinate2:
        newcolumn = point + coordinate
        OpenPosecolumns.append(newcolumn)
#print(body[OpenPosecolumns].shape)
selectedparts = body[OpenPosecolumns]
i = 15
frame = selectedparts[i:i+1].values
print(frame)
xyz = np.reshape(frame, (14,3))
x = xyz[:,0:1]
y = xyz[:,1:2]
z = xyz[:,2:]
#~~~~~~~~~~~~~~~~右鎖骨~~~~~~~~~~~~~~~~~~~~~~~~
x1 = x[0:2]
y1 = y[0:2]
z1 = z[0:2]
#print(x1)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~左鎖骨~~~~~~~~~~~~~~~~~~~~~~~~
x2 = [x[0],x[2]]
y2 = [y[0],y[2]]
z2 = [z[0],z[2]]
#print(x1)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~背筋~~~~~~~~~~~~~~~~~~~~~~~~
x3 = [x[0],x[7]]
y3 = [y[0],y[7]]
z3 = [z[0],z[7]]
#print(x1)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~右腕部~~~~~~~~~~~~~~~~~~~~~~~~
x4 = [x[1],x[3]]
y4 = [y[1],y[3]]
z4 = [z[1],z[3]]
#print(x1)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~左腕部~~~~~~~~~~~~~~~~~~~~~~~~
x5 = [x[2],x[4]]
y5 = [y[2],y[4]]
z5 = [z[2],z[4]]
#print(x1)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~右前腕部~~~~~~~~~~~~~~~~~~~~~~~~
x6 = [x[3],x[5]]
y6 = [y[3],y[5]]
z6 = [z[3],z[5]]
#print(x1)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~左前腕部~~~~~~~~~~~~~~~~~~~~~~~~
x7 = [x[4],x[6]]
y7 = [y[4],y[6]]
z7 = [z[4],z[6]]
#print(x1)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~右骨盤~~~~~~~~~~~~~~~~~~~~~~~
x8 = [x[7],x[8]]
y8 = [y[7],y[8]]
z8 = [z[7],z[8]]
#print(x1)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~左骨盤~~~~~~~~~~~~~~~~~~~~~~~
x9 = [x[7],x[9]]
y9 = [y[7],y[9]]
z9 = [z[7],z[9]]
#print(x1)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~右大腿~~~~~~~~~~~~~~~~~~~~~~~
x10 = [x[8],x[10]]
y10 = [y[8],y[10]]
z10 = [z[8],z[10]]
#print(x1)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~左大腿~~~~~~~~~~~~~~~~~~~~~~~
x11 = [x[9],x[11]]
y11 = [y[9],y[11]]
z11 = [z[9],z[11]]
#print(x1)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~右すね~~~~~~~~~~~~~~~~~~~~~~~
x12 = [x[10],x[12]]
y12 = [y[10],y[12]]
z12 = [z[10],z[12]]
#print(x1)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~左すね~~~~~~~~~~~~~~~~~~~~~~~
x13 = [x[11],x[13]]
y13 = [y[11],y[13]]
z13 = [z[11],z[13]]
#print(x1)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#x, y, z = np.random.multivariate_normal(np.array([0,0,0]), np.eye(3), 200).transpose()
trace1 = go.Scatter3d(
    x=x,
    y=y,
    z=z,
    mode='markers',
    marker=dict(
        size=5,
        line=dict(
            color='rgba(217, 217, 217, 0.14)',
            width=100
        ),
        opacity=0.8
    )
    )
trace2 = go.Scatter3d(
    x=x1,
    y=y1,
    z=z1,
    mode='lines',
        line=dict(
            color='rgba(0, 255, 0, 0.8)',
            width=10
        ),
        opacity=0.8
    )
trace3 = go.Scatter3d(
    x=x2,
    y=y2,
    z=z2,
    mode='lines',
        line=dict(
            color='rgba(0, 255, 0, 0.8)',
            width=10
        ),
        opacity=0.8
    )
trace4 = go.Scatter3d(
    x=x3,
    y=y3,
    z=z3,
    mode='lines',
        line=dict(
            color='rgba(0, 255, 0, 0.8)',
            width=10
        ),
        opacity=0.8
    )
trace5 = go.Scatter3d(
    x=x4,
    y=y4,
    z=z4,
    mode='lines',
        line=dict(
            color='rgba(0, 255, 0, 0.8)',
            width=10
        ),
        opacity=0.8
    )
trace6 = go.Scatter3d(
    x=x5,
    y=y5,
    z=z5,
    mode='lines',
        line=dict(
            color='rgba(0, 255, 0, 0.8)',
            width=10
        ),
        opacity=0.8
    )
trace7 = go.Scatter3d(
    x=x6,
    y=y6,
    z=z6,
    mode='lines',
        line=dict(
            color='rgba(0, 255, 0, 0.8)',
            width=10
        ),
        opacity=0.8
    )
trace8 = go.Scatter3d(
    x=x7,
    y=y7,
    z=z7,
    mode='lines',
        line=dict(
            color='rgba(0, 255, 0, 0.8)',
            width=10
        ),
        opacity=0.8
    )
trace9 = go.Scatter3d(
    x=x8,
    y=y8,
    z=z8,
    mode='lines',
        line=dict(
            color='rgba(0, 255, 0, 0.8)',
            width=10
        ),
        opacity=0.8
    )
trace10 = go.Scatter3d(
    x=x9,
    y=y9,
    z=z9,
    mode='lines',
        line=dict(
            color='rgba(0, 255, 0, 0.8)',
            width=10
        ),
        opacity=0.8
    )
trace11 = go.Scatter3d(
    x=x10,
    y=y10,
    z=z10,
    mode='lines',
        line=dict(
            color='rgba(0, 255, 0, 0.8)',
            width=10
        ),
        opacity=0.8
    )
trace12 = go.Scatter3d(
    x=x11,
    y=y11,
    z=z11,
    mode='lines',
        line=dict(
            color='rgba(0, 255, 0, 0.8)',
            width=10
        ),
        opacity=0.8
    )
trace13 = go.Scatter3d(
    x=x12,
    y=y12,
    z=z12,
    mode='lines',
        line=dict(
            color='rgba(0, 255, 0, 0.8)',
            width=10
        ),
        opacity=0.8
    )
trace14 = go.Scatter3d(
    x=x13,
    y=y13,
    z=z13,
    mode='lines',
        line=dict(
            color='rgba(0, 255, 0, 0.8)',
            width=10
        ),
        opacity=0.8
    )
data = [trace1,trace2,trace3,trace4,trace5,trace6,trace7,\
trace8,trace9,trace10,trace11,trace12,trace13,trace14]
"""
layout = go.Layout(
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=0
    )
)
"""
layout = go.Layout(
                    scene = dict(
                    xaxis = dict(
                        nticks=4, range = [-3,3],),
                    yaxis = dict(
                        nticks=4, range = [-3,3],),
                    zaxis = dict(
                        nticks=4, range = [-3,3],),),
                    width=700,
                    margin=dict(
                    r=0, l=0,
                    b=0, t=0)
                  )
fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='simple-3d-scatter')
