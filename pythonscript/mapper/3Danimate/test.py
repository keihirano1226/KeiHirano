import plotly
import pandas as pd
import chart_studio.plotly as py
import plotly.graph_objs as go

#import plotly.express as px
#plotly.tools.set_credentials_file(username='KeiHirano', api_key='krRfYzDQXbS3sZcZcpAf')
import numpy as np
import plotly.offline as offline

body = pd.read_csv("/home/kei/document/experiments/method/1,3_result/AveragePose1.csv", index_col = 0)
Frame = []
for i in range(len(body)):
    Frame.append(i)
body["Frame"] = Frame
"""
scatter = px.scatter_3d(body, x = "MidHipX", y = "MidHipY", z = "MidHipZ",animation_frame="Frame", trendline="ols")
#scatter
"""
x = body["MidHipX"].values
y = body["MidHipY"].values
z = body["MidHipZ"].values
scatter = go.Scatter3d(x=x, y=y, z=z, mode='lines', line=dict(width=2, color='blue'))


layout = dict(xaxis=dict(range=[x.min(), x.max()], autorange=False, zeroline=False),
              yaxis=dict(range=[y.min(), y.max()], autorange=False, zeroline=False),
              zaxis=dict(range=[z.min(), z.max()], autorange=False, zeroline=False),
              title='Gyro Motion of Electron', hovermode='closest',
              autosize=True,
              scene=dict(
                        aspectratio=dict(x=0.4, y=0.4, z=1.6),
                        # aspectratio=dict(x=2, y=0.4, z=0.4), # ExB用
                        ),
              updatemenus=[{'type': 'buttons',
                            'buttons': [{'label': 'Play',
                                         'method': 'animate',
                                         'args':[None, dict(frame=dict(duration=0, redraw=False),
                                                 transition=dict(duration=0),
                                                 fromcurrent=True,
                                                 mode='immediate')]
                                         },
                                        {
                                            'args': [[None], {'frame': {'duration': 0, 'redraw': False},
                                                              'mode': 'immediate',
                                                              'transition': {'duration': 0}}],
                                            'label': 'Pause',
                                            'method': 'animate'
                                        }
                                        ]}])

frames = [dict(data=[dict(x=[x[k]],
                          y=[y[k]],
                          z=[z[k]],
                          mode='markers',
                          marker=dict(color='red', size=4)
                          )
                     ]) for k in range(len(x))]

figure = dict(data=scatter,frames=frames)
offline.plot(figure, filename='test.html')
