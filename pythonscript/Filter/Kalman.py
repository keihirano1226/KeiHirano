import numpy as np
import pandas as pd
import sys

def forward(matrix, start_dev, dev_q, dev_r):
    #start_devとdev_qはランダムウォークに従う．
    #高齢者の歩行速度を参考に1ステップあたり1/30mが妥当であると考えられる．
    #
    x_prev_ = [matrix[0]]
    P_prev_ = [start_dev]
    K_ = [P_prev_[0] / (P_prev_[0] + dev_r)]
    P_ = [dev_r * P_prev_[0] / (P_prev_[0] + dev_r)]
    x_ = [x_prev_[0] + K_[0] * (matrix[0] - x_prev_[0])]
    for t in range(1,len(matrix)):
        x_prev_.append(x_[t-1])
        P_prev_.append(P_[t-1] + dev_q)

        K_.append(P_prev_[t] / (P_prev_[t] + dev_r))
        x_.append(x_prev_[t] + K_[t] * (matrix[t] - x_prev_[t]))
        P_.append(dev_r * P_prev_[t] / (P_prev_[t] + dev_r))

    return x_

if __name__=='__main__':
    csvpass = "/home/kei/document/experiments/ICTH2019/SY01/3dboneRotated.csv"
    df = pd.read_csv(csvpass)
    df2 = df.Frame.values
    df2 = np.reshape(df2, (len(df2), 1))
    print(df2.shape)
    for column_name, item in df.iteritems():
        if column_name != "Frame":
            FilteredX = forward(item, 0.008, 0.008, 4)
            s = pd.Series(FilteredX)
            sn = s.values
            sn = np.reshape(sn, (len(sn), 1))
            df2 = np.concatenate([df2, sn], 1)
    #X = df.RSholderX.values
    #FilteredX = forward(X, 0.008, 0.008, 4)
    #print(type(FilteredX))
    #s = pd.Series(FilteredX)
    dfall = pd.DataFrame(data = df2, columns = df.columns)
    dfall.to_csv("/home/kei/document/experiments/ICTH2019/SY01/FilteredRShouldered.csv",index = 0)
