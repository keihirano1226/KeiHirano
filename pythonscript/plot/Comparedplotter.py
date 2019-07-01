import plotly
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
plotly.tools.set_credentials_file(username='KeiHirano', api_key='krRfYzDQXbS3sZcZcpAf')
import numpy as np

class Bone:
    def __init__(self,frame,color):
        self.xyz0 = np.reshape(frame, (14,3))
        self.x0 = self.xyz0[:,0:1]
        self.y0 = self.xyz0[:,1:2]
        self.z0 = self.xyz0[:,2:]

        #~~~~~~~~~~~~~~~~右鎖骨~~~~~~~~~~~~~~~~~~~~~~~~
        self.x1 = self.x0[0:2]
        self.y1 = self.y0[0:2]
        self.z1 = self.z0[0:2]
        #print(x1)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #~~~~~~~~~~~~~~~~左鎖骨~~~~~~~~~~~~~~~~~~~~~~~~
        self.x2 = [self.x0[0],self.x0[2]]
        self.y2 = [self.y0[0],self.y0[2]]
        self.z2 = [self.z0[0],self.z0[2]]
        #print(x1)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #~~~~~~~~~~~~~~~~背筋~~~~~~~~~~~~~~~~~~~~~~~~
        self.x3 = [self.x0[0],self.x0[7]]
        self.y3 = [self.y0[0],self.y0[7]]
        self.z3 = [self.z0[0],self.z0[7]]
        #print(x1)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #~~~~~~~~~~~~~~~~右腕部~~~~~~~~~~~~~~~~~~~~~~~~
        self.x4 = [self.x0[1],self.x0[3]]
        self.y4 = [self.y0[1],self.y0[3]]
        self.z4 = [self.z0[1],self.z0[3]]
        #print(x1)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #~~~~~~~~~~~~~~~~左腕部~~~~~~~~~~~~~~~~~~~~~~~~
        self.x5 = [self.x0[2],self.x0[4]]
        self.y5 = [self.y0[2],self.y0[4]]
        self.z5 = [self.z0[2],self.z0[4]]
        #print(x1)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #~~~~~~~~~~~~~~~~右前腕部~~~~~~~~~~~~~~~~~~~~~~~~
        self.x6 = [self.x0[3],self.x0[5]]
        self.y6 = [self.y0[3],self.y0[5]]
        self.z6 = [self.z0[3],self.z0[5]]
        #print(x1)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #~~~~~~~~~~~~~~~~左前腕部~~~~~~~~~~~~~~~~~~~~~~~~
        self.x7 = [self.x0[4],self.x0[6]]
        self.y7 = [self.y0[4],self.y0[6]]
        self.z7 = [self.z0[4],self.z0[6]]
        #print(x1)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #~~~~~~~~~~~~~~~~~右骨盤~~~~~~~~~~~~~~~~~~~~~~~
        self.x8 = [self.x0[7],self.x0[8]]
        self.y8 = [self.y0[7],self.y0[8]]
        self.z8 = [self.z0[7],self.z0[8]]
        #print(x1)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #~~~~~~~~~~~~~~~~~左骨盤~~~~~~~~~~~~~~~~~~~~~~~
        self.x9 = [self.x0[7],self.x0[9]]
        self.y9 = [self.y0[7],self.y0[9]]
        self.z9 = [self.z0[7],self.z0[9]]
        #print(x1)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #~~~~~~~~~~~~~~~~~右大腿~~~~~~~~~~~~~~~~~~~~~~~
        self.x10 = [self.x0[8],self.x0[10]]
        self.y10 = [self.y0[8],self.y0[10]]
        self.z10 = [self.z0[8],self.z0[10]]
        #print(x1)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #~~~~~~~~~~~~~~~~~左大腿~~~~~~~~~~~~~~~~~~~~~~~
        self.x11 = [self.x0[9],self.x0[11]]
        self.y11 = [self.y0[9],self.y0[11]]
        self.z11 = [self.z0[9],self.z0[11]]
        #print(x1)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #~~~~~~~~~~~~~~~~~右すね~~~~~~~~~~~~~~~~~~~~~~~
        self.x12 = [self.x0[10],self.x0[12]]
        self.y12 = [self.y0[10],self.y0[12]]
        self.z12 = [self.z0[10],self.z0[12]]
        #print(x1)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #~~~~~~~~~~~~~~~~~左すね~~~~~~~~~~~~~~~~~~~~~~~
        self.y13 = [self.y0[11],self.y0[13]]
        self.x13 = [self.x0[11],self.x0[13]]
        self.z13 = [self.z0[11],self.z0[13]]
        #print(x1)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #self.a = np.random.randn(500)
        self.a = color
        #x, y, z = np.random.multivariate_normal(np.array([0,0,0]), np.eye(3), 200).transpose()
        self.trace1 = go.Scatter3d(
            x=self.x0,
            y=self.y0,
            z=self.z0,
            mode='markers',
            marker=dict(
                size=5,
                line=dict(
                    color='#377eb8',
                    width=100
                ),
                opacity=0.8
            )
            )
        self.trace2 = go.Scatter3d(
            x=self.x1,
            y=self.y1,
            z=self.z1,
            mode='lines',
                line=dict(
                    color=self.a,
                    width=10
                ),
                opacity=0.8
            )
        self.trace3 = go.Scatter3d(
            x=self.x2,
            y=self.y2,
            z=self.z2,
            mode='lines',
                line=dict(
                    color=self.a,
                    width=10
                ),
                opacity=0.8
            )
        self.trace4 = go.Scatter3d(
            x=self.x3,
            y=self.y3,
            z=self.z3,
            mode='lines',
                line=dict(
                    color=self.a,
                    width=10
                ),
                opacity=0.8
            )
        self.trace5 = go.Scatter3d(
            x=self.x4,
            y=self.y4,
            z=self.z4,
            mode='lines',
                line=dict(
                    color=self.a,
                    width=10
                ),
                opacity=0.8
            )
        self.trace6 = go.Scatter3d(
            x=self.x5,
            y=self.y5,
            z=self.z5,
            mode='lines',
                line=dict(
                    color=self.a,
                    width=10
                ),
                opacity=0.8
            )
        self.trace7 = go.Scatter3d(
            x=self.x6,
            y=self.y6,
            z=self.z6,
            mode='lines',
                line=dict(
                    color=self.a,
                    width=10
                ),
                opacity=0.8
            )
        self.trace8 = go.Scatter3d(
            x=self.x7,
            y=self.y7,
            z=self.z7,
            mode='lines',
                line=dict(
                    color=self.a,
                    width=10
                ),
                opacity=0.8
            )
        self.trace9 = go.Scatter3d(
            x=self.x8,
            y=self.y8,
            z=self.z8,
            mode='lines',
                line=dict(
                    color=self.a,
                    width=10
                ),
                opacity=0.8
            )
        self.trace10 = go.Scatter3d(
            x=self.x9,
            y=self.y9,
            z=self.z9,
            mode='lines',
                line=dict(
                    color=self.a,
                    width=10
                ),
                opacity=0.8
            )
        self.trace11 = go.Scatter3d(
            x=self.x10,
            y=self.y10,
            z=self.z10,
            mode='lines',
                line=dict(
                    color=self.a,
                    width=10
                ),
                opacity=0.8
            )
        self.trace12 = go.Scatter3d(
            x=self.x11,
            y=self.y11,
            z=self.z11,
            mode='lines',
                line=dict(
                    color=self.a,
                    width=10
                ),
                opacity=0.8
            )
        self.trace13 = go.Scatter3d(
            x=self.x12,
            y=self.y12,
            z=self.z12,
            mode='lines',
                line=dict(
                    color=self.a,
                    width=10
                ),
                opacity=0.8
            )
        self.trace14 = go.Scatter3d(
            x=self.x13,
            y=self.y13,
            z=self.z13,
            mode='lines',
                line=dict(
                    color=self.a,
                    width=10
                ),
                opacity=0.8
            )
class PoseReader():
    def __init__(self, csvpass, FrameNumber):
        self.csv = csvpass
        self.OpenPosecolumns = []
        self.Fn = FrameNumber
        self.OpenPoseJoint = ["Neck","RSholder","LSholder","RElbow","LElbow","RWrist","LWrist","MidHip",\
        "RHip","LHip","RKnee","LKnee","RAnkle","LAnkle"]
        self.Coordinate2 = ["X","Y","Z"]
        for point in self.OpenPoseJoint:
            for coordinate in self.Coordinate2:
                newcolumn = point + coordinate
                self.OpenPosecolumns.append(newcolumn)
        self.df = pd.read_csv(self.csv)
        self.body = self.df[self.OpenPosecolumns]
        self.Frame = self.body[self.Fn:self.Fn+1].values



#df1 = pd.read_csv("/home/kei/document/experiments/2019.06.25/data2/3dboneRotated.csv")

#df2 = pd.read_csv("/home/kei/document/experiments/2019.06.25/data3/3dboneRotated.csv")
csvpass1 = "/home/kei/document/experiments/2019.06.25/data2/GroundedPose.csv"
csvpass2 = "/home/kei/document/experiments/2019.06.25/data3/GroundedPose.csv"
posture1 = PoseReader(csvpass1,7)#真ん中
posture2 = PoseReader(csvpass1,15)#後ろ
posture3 = PoseReader(csvpass1,51)#前

bone1 = Bone(posture1.Frame,'#0000ff')
bone2 = Bone(posture2.Frame,'#008000')
bone3 = Bone(posture3.Frame,'#ffff00')
#print(frame)

data = [bone1.trace1,bone1.trace2,bone1.trace3,bone1.trace4,\
bone1.trace5,bone1.trace6,bone1.trace7,bone1.trace8,bone1.trace9,\
bone1.trace10,bone1.trace11,bone1.trace12,bone1.trace13,bone1.trace14,\
bone2.trace1,bone2.trace2,bone2.trace3,bone2.trace4,\
bone2.trace5,bone2.trace6,bone2.trace7,bone2.trace8,bone2.trace9,\
bone2.trace10,bone2.trace11,bone2.trace12,bone2.trace13,bone2.trace14,\
bone3.trace1,bone3.trace2,bone3.trace3,bone3.trace4,\
bone3.trace5,bone3.trace6,bone3.trace7,bone3.trace8,bone3.trace9,\
bone3.trace10,bone3.trace11,bone3.trace12,bone3.trace13,bone3.trace14\
]

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
                        nticks=4, range = [-1.25,1.25],),
                    yaxis = dict(
                        nticks=4, range = [-1.25,1.25],),
                    zaxis = dict(
                        nticks=4, range = [-1.25,1.25],),),
                    width=700,
                    margin=dict(
                    r=0, l=0,
                    b=0, t=0)
                  )
fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='simple-3d-scatter')
