import numpy as np
import pandas as pd
import chart_studio.plotly as py
import plotly.graph_objs as go
import plotly.offline as offline
csvpass = "/home/kei/document/experiments/BioEngen/MA330_11/product/tra_3dpoints.csv"
points = pd.read_csv(csvpass)

x = points.x
y = points.y
z = points.z
fig = go.Figure(data=[go.Mesh3d(x=x, y=y, z=z, alphahull=1,color='lightpink', opacity=0.50)])
offline.plot(fig, filename = "/home/kei/document/experiments/BioEngen/MA330_11/product/product.html",auto_open=False)
