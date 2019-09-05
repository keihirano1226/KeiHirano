import pandas as pd
import numpy as np
import sys

class JointVector():
    def __init__(self, sp, gp1, gp2):
        self.vec1 = self.vec(sp, gp1)
        self.vec2 = self.vec(sp, gp2)

    def vec(self, start_point, goal_point):
        return goal_point - start_point

    def compute_angle(self):
        norm_vec1 = np.sqrt(np.diag(self.vec1 @ self.vec1.T))
        norm_vec2 = np.sqrt(np.diag(self.vec2 @ self.vec2.T))
        theta = np.arccos(np.diag(self.vec1 @ self.vec2.T) / (norm_vec1 * norm_vec2))
        return theta

# sp = np.array([[0, 0], [0, 0]])
# gp1 = np.array([[1, 0], [5, 0]])
# gp2 = np.array([[0, 1], [-8, 0]])

# jv = JointVector(sp, gp1, gp2)
# print(jv.compute_angle())
