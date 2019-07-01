岡田さんの被験者1で実施したもの
ZeroCenered.py
Coordinate.csvを読み込んで，骨盤原点のcentered.csvに置き換えるプログラム

PelvisRotation.py
骨盤をx軸，背筋をy軸にした座標系の変換するプログラム
出力はRotated.csv

ArmRotation.py
x軸を左肩から右肩へのベクトル、背筋をy軸にした座標系へ変換を行うプログラム
入力はRotated.csv,出力はArmRotated.csv

PelvisJointAngle.py
入力はPelvisRotationMatrix.csv
これの中身は[[R11,R12,R13]
           [R21,R22,R23]
           [R31,R32,R33]]
の行列が['R11','R12','R13','R21','R22','R23','R31','R32','R33']
の順で入っている
ここからオイラー角をそれぞれ計算していく

NormarizeLength.py
各座標値ベクトルを全て長さ1に変換して、
  spinal = 0
  Neck = 1
  ClavicleR = 2
  UpperarmR = 3
  ForearmR = 4
  ClavicleL = 5
  UpperarmL = 6
  ForearmL = 7
  PelvisR = 8
  FemurR = 9
  ShinR = 10
  PelvisL = 11
  FemurL = 12
  ShinL = 13
の順番でxyz座標値をNormarizedVector.csvに保存するプログラム

NormarizedPosition.py
各種座標値ベクトルの長さをすべて1にしたうえで、座標値を出すためのプログラム
出力のファイルはNormarizedPosition.csv

LegJointAngle.py
足の関節角度を計算するためのプログラム
読み込むのは、NormarizedVector.csv
計算できるのは、股関節屈曲、回旋、内転、膝関節屈曲
出力は、LegJointAngle.csv
というプログラム
