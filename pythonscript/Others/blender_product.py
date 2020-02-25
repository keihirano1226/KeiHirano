import csv
import math
import bpy

csvfile =  '/home/shoda/Documents/Image_processing/semaseg/product_xyz.csv'

f = open(csvfile,'r')
reader = csv.reader(f)
for i, row in enumerate(reader):
    if i == 500:
        break
    bpy.ops.mesh.primitive_ico_sphere_add(
            size=0.005,
            location=(float(row[0]), float(row[1]), float(row[2]))
        )
f.close()