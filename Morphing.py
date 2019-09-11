#######################################################
# Author: lin779
# email: lin779@purdue.edu
# ID: ee364g07
# Date: 2019.04.08
# #######################################################

from scipy.spatial import Delaunay
from scipy.interpolate import RectBivariateSpline as RB
import numpy as np
import imageio
import imageio_ffmpeg
import cv2
# imageio.plugins.ffmpeg.download()
from matplotlib import pyplot as plt
import os
import time
from matplotlib.path import Path
from scipy import ndimage
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication
from scipy import interpolate







DataPath = os.path.expanduser("~/Documents/2019S/ECE364/labs-duvme/Lab12")




def loadTriangles(leftPointFilePath, rightPointFilePath):
    lftpoints = np.array(np.loadtxt(leftPointFilePath))
    rgtpoints = np.array(np.loadtxt(rightPointFilePath))
    Del = Delaunay(lftpoints)
    temp1 = lftpoints[Del.simplices]
    temp2 = rgtpoints[Del.simplices]
    lft_triangles = []
    rgt_triangles = []
    for i in temp1:
        lft_triangles.append(Triangle(i))
    for j in temp2:
        rgt_triangles.append(Triangle(j))

    return (lft_triangles, rgt_triangles)


class Triangle:
    def __init__(self, vertices):
        if type(vertices) != np.ndarray:
            raise ValueError
        if vertices.shape != (3,2):
            raise ValueError("fuck you")
        if vertices.dtype != "float64":
            raise ValueError
        self.vertices = vertices

    def __str__(self):
        return str(self.vertices[0]) + ' , ' + str(self.vertices[1]) + ' , ' + str(self.vertices[2])

    def getPoints(self):
        col_max = int(max(self.vertices[0][0], self.vertices[1][0], self.vertices[2][0]) + 0.5)
        col_min = int(min(self.vertices[0][0], self.vertices[1][0], self.vertices[2][0]) + 0.5)
        row_max = int(max(self.vertices[0][1], self.vertices[1][1], self.vertices[2][1]) + 0.5)
        row_min = int(min(self.vertices[0][1], self.vertices[1][1], self.vertices[2][1]) + 0.5)
        x, y = np.meshgrid(np.arange(col_min, col_max + 1), np.arange(row_min, row_max + 1))
        x, y = x.flatten(), y.flatten()
        points = np.vstack((x, y)).T
        p = Path(self.vertices)
        grid = p.contains_points(points)
        return points[grid].astype(np.float64)


class Morpher:
    def __init__(self, leftImage, leftTriangles, rightImage, rightTriangles):
        if not self._all(leftTriangles) or not self._all(rightTriangles):
            raise TypeError
        if not isinstance(leftImage, np.ndarray) or not isinstance(leftImage, np.ndarray):
            raise TypeError
        if leftImage.dtype != "uint8" or rightImage.dtype != "uint8":
            raise TypeError

        self.leftImage = leftImage
        self.leftTriangles = leftTriangles
        self.rightImage = rightImage
        self.rightTriangles = rightTriangles

    def _all(self, elements):
        for i in elements:
            if not isinstance(i, Triangle):
                return False
        return True

    def getImageAtAlpha(self, alpha):
        if not isinstance(alpha, int):
            if not isinstance(alpha,float):
                raise TypeError
        if not 0 <= alpha <= 1:
            raise ValueError
        if alpha == 0:
            return self.leftImage
        elif alpha == 1:
            return self.rightImage

        a, b = self.leftImage.shape
        left_p = RB(x = np.arange(0, a), y = np.arange(0, b), z = self.leftImage, kx=1, ky=1)
        right_p = RB(x = np.arange(0, a), y = np.arange(0, b), z = self.rightImage, kx=1, ky=1)
        output = np.ones(self.leftImage.shape)

        for left, right in zip(self.leftTriangles, self.rightTriangles):
            target = Triangle((1 - alpha) * left.vertices + alpha * right.vertices)
            target_points = target.getPoints()  #n*2
            target_points_3 = np.column_stack((target_points, np.ones(len(target_points))))  #n*3

            temp_left = np.column_stack((left.vertices, np.ones(len(left.vertices))))
            temp_right = np.column_stack((right.vertices, np.ones(len(right.vertices))))
            temp_target = np.column_stack((target.vertices, np.ones(len(target.vertices))))

            temp = np.matmul(target_points_3, np.linalg.inv(temp_target))

            result_left = np.matmul(temp, temp_left).T
            result_right = np.matmul(temp, temp_right).T

            temp2 = (target_points.astype(int)).T
            #result = (1 - alpha) * result_left + alpha * result_right
            #output[temp2[0]] = result[0]
            #output[temp2[1]] = result[1]
            output[temp2[1], temp2[0]] = (1 - alpha) * left_p.ev(result_left[1], result_left[0]) + alpha * right_p.ev(result_right[1], result_right[0])

        output[0] = (1 - alpha) * self.leftImage[0] + alpha * self.rightImage[0]
        return output.astype(np.uint8)


    def saveVideo(self, targetFilePath, frameCount, frameRate, includeReversed):
        '''
        writer = imageio.get_writer(targetFilePath, fps = frameRate)
        count = 0
        reverse = []
        for i in range(frameCount, 0, -1):
            if i == 0:
                alpha = 0
            else:
                alpha = 1 / i
            writer.append_data(self.getImageAtAlpha(alpha))
            if includeReversed == True:
                reverse.append(self.getImageAtAlpha(alpha))
            count += 1
        reverse = reversed(reverse)
        for i in reverse:
            writer.append_data(i)
        writer.close()
        '''

        # fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        # videoWriter = cv2.VideoWriter(targetFilePath, fourcc, frameRate,(500, 750), 1)
        count = 0
        reverse = []
        for i in range(frameCount):
            if i == 0:
                alpha = 0
            else:
                alpha = i / frameCount
            imageio.imwrite(os.path.join(DataPath, "output/" + str(count) + ".jpg"), self.getImageAtAlpha(alpha))
            # if includeReversed == True:
            #     reverse.append(self.getImageAtAlpha(alpha))
            count += 1
        reverse = reversed(reverse)
        # for i in reverse:
        #     videoWriter.write(i)
        # videoWriter.release()



class ColorMorpher(Morpher):
    def __init__(self, leftImg, leftTriangles, rightImg, rightTriangles):
        super().__init__(leftImg, leftTriangles, rightImg, rightTriangles)

    def getImageAtAlpha(self, alpha):
        if not isinstance(alpha, int):
            if not isinstance(alpha,float):
                raise TypeError
        if not 0 <= alpha <= 1:
            raise ValueError

        a, b, c = self.leftImage.shape

        r_left_p = RB(x = np.arange(0, a), y = np.arange(0, b), z = self.leftImage[:,:,0], kx=1, ky=1)
        r_right_p = RB(x = np.arange(0, a), y = np.arange(0, b), z=self.rightImage[:,:,0], kx=1, ky=1)
        g_left_p = RB(x=np.arange(0, a), y=np.arange(0, b), z=self.leftImage[:,:,1], kx=1, ky=1)
        g_right_p = RB(x=np.arange(0, a), y=np.arange(0, b), z=self.rightImage[:,:,1], kx=1, ky=1)
        b_left_p = RB(x=np.arange(0, a), y=np.arange(0, b), z=self.leftImage[:,:,2], kx=1, ky=1)
        b_right_p = RB(x=np.arange(0, a), y=np.arange(0, b), z=self.rightImage[:,:,2], kx=1, ky=1)
        output = np.zeros(self.leftImage.shape)

        for left, right in zip(self.leftTriangles, self.rightTriangles):
            target = Triangle((1 - alpha) * left.vertices + alpha * right.vertices)
            target_points = target.getPoints()  # n*2
            target_points_3 = np.column_stack((target_points, np.ones(len(target_points))))  # n*3

            temp_left = np.column_stack((left.vertices, np.ones(len(left.vertices))))
            temp_right = np.column_stack((right.vertices, np.ones(len(right.vertices))))
            temp_target = np.column_stack((target.vertices, np.ones(len(target.vertices))))

            temp = np.matmul(target_points_3, np.linalg.inv(temp_target))

            result_left = np.matmul(temp, temp_left).T
            result_right = np.matmul(temp, temp_right).T

            temp2 = (target_points.astype(int)).T
            # target_tri = Triangle((1 - alpha) * left.vertices + alpha * right.vertices)
            # h_left = self._calc_h(target_tri, left)
            # h_right = self._calc_h(target_tri, right)
            #
            # h_left = np.linalg.inv(h_left)
            # h_right = np.linalg.inv(h_right)
            #
            # target_points = target_tri.getPoints()  #n*2
            # target_points_3 = np.column_stack((target_points, np.ones(len(target_points)))) #n*3
            #
            # result_left = np.matmul(h_left, target_points_3.T)
            # result_right = (h_right @ target_points_3.T)[0:2]
            # temp2 = (target_points.astype(int)).T

            output[temp2[1], temp2[0],0] = (1 - alpha) * r_left_p.ev(result_left[1], result_left[0]) + alpha * r_right_p.ev(result_right[1], result_right[0])
            output[temp2[1], temp2[0],1] = (1 - alpha) * g_left_p.ev(result_left[1], result_left[0]) + alpha * g_right_p.ev(result_right[1], result_right[0])
            output[temp2[1], temp2[0],2] = (1 - alpha) * b_left_p.ev(result_left[1], result_left[0]) + alpha * b_right_p.ev(result_right[1], result_right[0])

        output[0,:,0] = (1 - alpha) * self.leftImage[0,:,0] + alpha * self.rightImage[0,:,0]
        output[0,:,1] = (1 - alpha) * self.leftImage[0,:,1] + alpha * self.rightImage[0,:,1]
        output[0,:,2] = (1 - alpha) * self.leftImage[0,:,2] + alpha * self.rightImage[0,:,2]
        return output.astype(np.uint8)


if __name__ == "__main__":
    path = os.path.join(DataPath,'TestData')
    (left_tri, right_tri) = loadTriangles(os.path.join(DataPath, 'gjw.jpg.txt'), os.path.join(DataPath, 'lgz.jpg.txt'))
    #(left_tri, right_tri) = loadTria
    # ngles(os.path.join(path,'points.left.txt'), os.path.join(path,'points.right.txt'))
    leftImg = np.array(imageio.imread(os.path.join(DataPath,"gjw.jpg")))
    rightImg = np.array(imageio.imread(os.path.join(DataPath,"lgz.jpg")))

    mr = ColorMorpher(leftImg, left_tri, rightImg, right_tri)
    # x = mr.getImageAtAlpha(0.5)

    a = mr.saveVideo('zcnh.mp4',50, 5, False)
    start = time.time()
    print(time.time() - start)

    #plt.imsave('linyanzu.png', x, cmap = 'gray')

    #c_leftImg = np.array(imageio.imread(os.path.join(path, "LeftColor.png")))
    #c_rightImg = np.array(imageio.imread(os.path.join(path, "RightColor.png")))
    #c_mr = ColorMorpher(c_leftImg, left_tri, c_rightImg, right_tri)
    #x = c_mr.getImageAtAlpha(0.5)
    #plt.imsave('color.png', x, cmap='gray')




