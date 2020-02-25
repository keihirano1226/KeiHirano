import csv
import math
import bpy

csvfile =  '/home/shoda/Documents/3danalyze/3dboneRotated.csv'
#csvfile =  '/home/shoda/Documents/mitsu/3dbone_fixed.csv'

f = open(csvfile,'r')
reader = csv.reader(f)
header = next(reader)

for i, row in enumerate(reader):
    del row[0]
    #del row[1]
    for j in range(25):

        if not (row[3*j + 0] or row[3*j + 1] or row[3*j + 2]):
            continue
        
        if j == 0:
            bpy.context.scene.frame_set(i)
            bpy.data.objects["Icosphere"].location.x = float(row[3*j + 0])*1
            bpy.data.objects["Icosphere"].location.y = float(row[3*j + 1])*1
            bpy.data.objects["Icosphere"].location.z = float(row[3*j + 2])*1
            bpy.ops.anim.keyframe_insert_menu(type="Location")
        else:
            bpy.context.scene.frame_set(i)
            bpy.data.objects["Icosphere." + str('{:0=3}'.format(j))].location.x = float(row[3*j + 0])*1
            bpy.data.objects["Icosphere." + str('{:0=3}'.format(j))].location.y = float(row[3*j + 1])*1
            bpy.data.objects["Icosphere." + str('{:0=3}'.format(j))].location.z = float(row[3*j + 2])*1
            bpy.ops.anim.keyframe_insert_menu(type="Location")

        print(i)
f.close()