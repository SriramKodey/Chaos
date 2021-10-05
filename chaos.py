import numpy as np
import cv2
import math
import random
import sys

def euclidean(a, b):
    dist = math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
    return dist

class image:
    def __init__(self, height, width):
        self.height = height
        self.width = width

        self.img = np.zeros([self.height, self.width], dtype = np.uint8)

    def make_bugs(self, num_bugs):
        self.x_size = int(self.width/5)
        self.y_size = int(self.height/5)
        self.num_bugs = num_bugs
        
        bugs = np.random.choice(self.x_size*self.y_size, num_bugs)

        self.points = []

        self.blink_rate = np.zeros(num_bugs)

        for i in range(num_bugs):
            x = bugs[i] % self.x_size
            y = int(bugs[i] / self.y_size)

            self.points.append((x, y))

            self.blink_rate[i] = np.random.choice(50, 1)[0]

    def generate_dist_matrix(self):
        self.dist_mat = np.zeros([self.num_bugs, self.num_bugs])

        for i in range(self.num_bugs):
            for j in range(self.num_bugs):
                if i == j:
                    self.dist_mat[i][j] = 65535

                else:
                    self.dist_mat[i][j] = euclidean(self.points[i], self.points[j])

        
    def switch_bugs_on(self, pos):
        for i in pos:
            x = self.points[i][0]
            y = self.points[i][1]

            for j in range(5):
                for k in range(5):
                    self.img[5*x + j][5*y + k] = 255

    def switch_bugs_off(self, pos):
        for i in pos:
            x = self.points[i][0]
            y = self.points[i][1]

            for j in range(5):
                for k in range(5):
                    self.img[5*x + j][5*y + k] = 0

    def update_blink_rate(self):
        for i in range(self.num_bugs):
            self.blink_rate[i] = self.blink_rate[np.where(self.dist_mat[i] == min(self.dist_mat[i]))[0][0]]

    def normal_blink(self):
        while(True):
            for k in range(75):
                ## Switch On bugs
                self.switch_bugs_on(np.where(self.blink_rate == k)[0])

                ## Switch Off Bugs
                self.switch_bugs_off(np.where(self.blink_rate+15 == k)[0])

                cv2.imshow("vid", self.img)
                cv2.waitKey(40)

            self.update_blink_rate()


def main(height, width):
    frame = image(height, width)

    frame.make_bugs(100)

    frame.generate_dist_matrix()

    frame.normal_blink()
    

if __name__ == "__main__":

    height = 500
    width = 500



    main(500, 500)

