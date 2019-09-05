#距離行列計算用
OpenPoseJoint = ["Neck","RSholder","LSholder","RElbow","LElbow","LWrist","RWrist","MidHip","RHip","LHip","RKnee","LKnee","RAnkle","LAnkle"]
Coordinate = ["X","Y","Z"]
bodycolumns = []
MainJointAngleList = [['RSholder', 'Neck', 'RElbow'], ['RElbow', 'RSholder', 'RWrist'], ['RHip', 'MidHip', 'RKnee'], ['RKnee', 'RHip', 'RAnkle'],
                      ['LSholder', 'Neck', 'LElbow'], ['LElbow', 'LSholder', 'LWrist'], ['LHip', 'MidHip', 'LKnee'], ['LKnee', 'LHip', 'LAnkle']]
for point in OpenPoseJoint:
    for coordinate in Coordinate:
        newcolumn = point + coordinate
        bodycolumns.append(newcolumn)

#関節名から関節座標名への変換
def joint2coordinate(name):
    return list(map(lambda x : name + x, Coordinate))

