import sys
from PIL.ImageQt import ImageQt
from PIL import Image
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Morphing import *
from MorphingGUI import *
import time
import imageio
import numpy as np


class MorphingApp(QMainWindow, Ui_MainWindow, QWidget):
    def __init__(self, parent=None):
        super(MorphingApp, self).__init__(parent)
        self.setupUi(self)

        self.initial_state()
        self.check1 = False
        self.button = False
        self.check2 = False
        self.left_scene = QGraphicsScene()
        self.right_scene = QGraphicsScene()
        self.prev_left = tuple()
        self.prev_right = tuple()
        self.left_drew = False
        self.right_drew = True
        self.drew = False
        self.original = False
        self.pair = []
        self.alpha = 0.0

        # connect start button with load image and show the image
        self.btn_start.clicked.connect(self.load_start_image)

        # connect end button with load right image and show the image
        self.btn_end.clicked.connect(self.load_end_image)

        # connect blend button with morpher
        self.btn_blend.clicked.connect(self.do_Morpher)

        # from silde bar value to obtain alpha value
        self.slide_bar.valueChanged[int].connect(self.valuechange)

        # check box to show triangle
        self.check_triangles.stateChanged.connect(self.show_triangles)

        # get input alpha value and set it to slide bar
        # self.edit_alpha.textEdited.connect(self.set_slide)

    def show_triangles(self):
        if self.check_triangles.isChecked():
            if self.original is True and self.drew is False:
                self.draw_tri(Qt.red)
            elif self.drew is True and self.original is False:
                self.draw_tri(Qt.blue)
            elif self.drew is True and self.original is True:
                self.draw_tri(Qt.darkCyan)
        else:
            self.remove_tri()

    def remove_tri(self):
        for item in self.left_scene.items():
            if isinstance(item, QGraphicsPolygonItem):
                self.left_scene.removeItem(item)
        for item in self.right_scene.items():
            if isinstance(item, QGraphicsPolygonItem):
                self.right_scene.removeItem(item)


    def draw_tri(self, color):
        (lft, rgt) = xixi_loadTriangles(self.left_txt_path, self.right_txt_path, self.ratio)
        for tri in lft:
            one = QPointF(tri.vertices[0][0], tri.vertices[0][1])
            two = QPointF(tri.vertices[1][0], tri.vertices[1][1])
            three = QPointF(tri.vertices[2][0], tri.vertices[2][1])
            self.left_scene.addPolygon(QPolygonF([one, two, three]), QPen(color, 1, cap=Qt.RoundCap))
        for tri in rgt:
            one = QPointF(tri.vertices[0][0], tri.vertices[0][1])
            two = QPointF(tri.vertices[1][0], tri.vertices[1][1])
            three = QPointF(tri.vertices[2][0], tri.vertices[2][1])
            self.right_scene.addPolygon(QPolygonF([one, two, three]), QPen(color, 1, cap=Qt.RoundCap))

    def set_slide(self):
        if self.edit_alpha.text() != '':
            num = float(self.edit_alpha.text())
            num = int(num * 100)
            self.slide_bar.setValue(num)

    def valuechange(self, value):
        self.alpha = float(int((value + 2) / 5) / 20)
        self.edit_alpha.setText(str(self.alpha))
        if self.button is True :
            self.pic.clear()
            self.pic.setPixmap(self.plst[int(self.alpha / 0.05)])
            self.pic.show()

    def mousePressEvent(self, e):
        if self.check1 is True and self.check2 is True:
            self.fp_left = open(self.left_txt_path, "a+")
            self.fp_right = open(self.right_txt_path, "a+")
            if 30 <= e.pos().x() <= self.box_start.width() + 30 and 50 <= e.pos().y() <= self.box_start.height() + 50:
                if self.right_drew is True:
                    if len(self.pair) == 2:
                        self.left_scene.addEllipse(self.pair[0][0],self.pair[0][1], 2, 2, QPen(Qt.blue, 2, cap=Qt.RoundCap))
                        self.right_scene.addEllipse(self.pair[1][0],self.pair[1][1], 2, 2, QPen(Qt.blue, 2, cap=Qt.RoundCap))
                        self.fp_left.write(str(self.pair[0][0]/self.ratio) + "\t" + str(self.pair[0][1]/self.ratio) + "\n")
                        self.fp_right.write(str(self.pair[1][0]/self.ratio) + "\t" + str(self.pair[1][1]/self.ratio) + "\n")
                        self.fp_right.close()
                        self.fp_left.close()
                        self.pair = []
                        self.drew = True
                        self.remove_tri()
                        self.show_triangles()
                    self.left_scene.addEllipse(e.pos().x() - 30, e.pos().y() - 50, 2, 2, QPen(Qt.green, 2, cap=Qt.RoundCap))
                    self.right_drew = False
                    self.left_drew = True
                    self.pair.append((e.pos().x() - 30, e.pos().y() - 50))

            elif 480 <= e.pos().x() <= self.box_end.width() + 480 and 50 <= e.pos().y() <= self.box_end.height() + 50:
                if self.left_drew is True:
                    self.right_scene.addEllipse(e.pos().x() - 480, e.pos().y() - 50, 2, 2, QPen(Qt.green, 2, cap=Qt.RoundCap))
                    self.right_drew = True
                    self.left_drew = False
                    self.pair.append((e.pos().x() - 480, e.pos().y() - 50))

            else:
                if len(self.pair) == 2:
                    self.left_scene.addEllipse(self.pair[0][0], self.pair[0][1], 2, 2, QPen(Qt.blue, 2, cap=Qt.RoundCap))
                    self.right_scene.addEllipse(self.pair[1][0], self.pair[1][1], 2, 2, QPen(Qt.blue, 2, cap=Qt.RoundCap))
                    self.fp_left.write(str(self.pair[0][0]/self.ratio) + "\t" + str(self.pair[0][1]/self.ratio) + "\n")
                    self.fp_right.write(str(self.pair[1][0]/self.ratio) + "\t" + str(self.pair[1][1]/self.ratio) + "\n")
                    self.fp_right.close()
                    self.fp_left.close()
                    self.pair = []
                    self.drew = True
                    self.remove_tri()
                    self.show_triangles()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Backspace:
            if len(self.pair) == 2:
                self.right_scene.removeItem(self.right_scene.items()[0])
                self.pair = self.pair[:-1]
                self.right_drew = False
                self.left_drew = True
            elif len(self.pair) == 1:
                self.left_scene.removeItem(self.left_scene.items()[0])
                self.pair = []
                self.right_drew = True
                self.left_drew = False
        if event.key() == Qt.Key_Alt:
            self.fp_left.close()
            self.fp_right.close()

    def show_start_image(self):
        self.left_scene.clear()
        self.box_start.resize(360, 270)
        pixmap = QPixmap(self.left_path)
        pixmap = pixmap.scaled(self.box_start.size(), Qt.KeepAspectRatio)
        self.box_start.resize(pixmap.size())

        self.left_scene.addPixmap(pixmap)
        self.box_start.setScene(self.left_scene)
        self.box_start.fitInView(self.left_scene.sceneRect(), Qt.KeepAspectRatio)
        self.check1 = True
        self.ratio = 270 / len(self.leftimage) * 0.99
        for point in self.left_txt:
            self.left_scene.addEllipse(point[0] * self.ratio, point[1] * self.ratio, 2, 2, QPen(Qt.red, 2, cap=Qt.RoundCap))

    def show_end_image(self):
        self.right_scene.clear()
        self.box_end.resize(360, 270)
        pixmap = QPixmap(self.right_path)
        pixmap = pixmap.scaled(self.box_end.size(), Qt.KeepAspectRatio)
        self.box_end.resize(pixmap.size())
        self.right_scene.addPixmap(pixmap)
        self.box_end.setScene(self.right_scene)
        self.box_end.fitInView(self.right_scene.sceneRect(), Qt.KeepAspectRatio)

        for point in self.right_txt:
            self.right_scene.addEllipse(point[0] * self.ratio, point[1] * self.ratio, 2, 2, QPen(Qt.red, 2, cap=Qt.RoundCap))


        self.check_triangles.setEnabled(True)
        self.btn_blend.setEnabled(True)
        self.slide_bar.setEnabled(True)
        self.edit_alpha.setEnabled(True)
        self.check2 = True

    def load_start_image(self):
        self.left_txt = []
        self.drew = False
        self.original = False

        self.left_path, _ = QFileDialog.getOpenFileName(None, 'OpenFile', '', 'Image file(*.png or *.jpg)')
        self.left_txt_path = self.left_path + '.txt'
        try:
            self.left_txt = np.loadtxt(self.left_txt_path)
            if len(self.left_txt) >= 3:
                self.original = True
        except:
            pass
        self.leftimage = np.array(imageio.imread(self.left_path))
        self.show_start_image()

    def load_end_image(self):
        self.right_txt = []
        self.right_path, _ = QFileDialog.getOpenFileName(None, 'OpenFile', '', 'Image file(*.png or  *.jpg)')
        self.right_txt_path = self.right_path + '.txt'
        try:
            self.right_txt = np.loadtxt(self.right_txt_path)
            if len(self.right_txt) >= 3:
                self.original = True
        except:
            pass
        self.rightimage = np.array(imageio.imread(self.right_path))
        self.show_end_image()

    def initial_state(self):
        self.edit_alpha.setText("0.0")
        self.check_triangles.setDisabled(True)
        self.btn_blend.setDisabled(True)
        self.slide_bar.setDisabled(True)
        self.edit_alpha.setDisabled(True)


    def do_Morpher(self):
        start = time.time()
        self.button = True
        self.leftimage = Image.open(self.left_path)
        self.leftimage.thumbnail((360,270))
        self.leftimage = np.array(self.leftimage)
        self.rightimage = Image.open(self.right_path)
        self.rightimage.thumbnail((360,270))
        self.rightimage = np.array(self.rightimage)
        self.plst = []
        if len(self.leftimage.shape) == 3 and len(self.rightimage.shape) == 3:
            (left_tri, right_tri) = xixi_loadTriangles(self.left_txt_path, self.right_txt_path, self.ratio)
            morpher = ColorMorpher(self.leftimage, left_tri, self.rightimage, right_tri)
            result_image = morpher.getImageAtAlpha(self.alpha)
            image = QImage(result_image, result_image.shape[1], result_image.shape[0], result_image.shape[1] * 3, QImage.Format_RGB888)
            self.pic = QLabel(self.box_result)
            pixmap = QPixmap(image)
            pixmap = pixmap.scaled(self.box_result.size(), Qt.KeepAspectRatio)
            self.pic.setPixmap(pixmap)
            self.box_result.resize(pixmap.size())
            self.pic.show()
            for i in range(0,21):
                result_image = morpher.getImageAtAlpha(i * 0.05)
                image = QImage(result_image, result_image.shape[1], result_image.shape[0],result_image.shape[1] * 3, QImage.Format_RGB888)
                pixmap = QPixmap(image)
                pixmap = pixmap.scaled(self.box_result.size(), Qt.KeepAspectRatio)
                self.plst.append(pixmap)
        elif len(self.leftimage.shape) == 2 and len(self.rightimage.shape) == 2:
            (left_tri, right_tri) = xixi_loadTriangles(self.left_txt_path, self.right_txt_path, self.ratio)
            morpher = Morpher(self.leftimage, left_tri, self.rightimage, right_tri)
            result_image = morpher.getImageAtAlpha(self.alpha)
            image = QImage(result_image, result_image.shape[1], result_image.shape[0],result_image.shape[1], QImage.Format_Grayscale8)
            self.pic = QLabel(self.box_result)
            pixmap = QPixmap(image)
            pixmap = pixmap.scaled(self.box_result.size(), Qt.KeepAspectRatio)
            self.pic.setPixmap(pixmap)
            self.box_result.resize(pixmap.size())
            self.pic.show()
            for i in range(0,21):
                result_image = morpher.getImageAtAlpha(i * 0.05)
                image = QImage(result_image, result_image.shape[1], result_image.shape[0],result_image.shape[1], QImage.Format_Grayscale8)
                pixmap = QPixmap(image)
                pixmap = pixmap.scaled(self.box_result.size(), Qt.KeepAspectRatio)
                self.plst.append(pixmap)
        else:
            raise TypeError
        print(time.time() - start)


def xixi_loadTriangles(leftPointFilePath, rightPointFilePath, scale):
    lftpoints = np.array(np.loadtxt(leftPointFilePath)) * scale
    rgtpoints = np.array(np.loadtxt(rightPointFilePath)) * scale
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

if __name__ == "__main__":
    currentApp = QApplication(sys.argv)
    currentForm = MorphingApp()
    currentForm.show()
    currentApp.exec_()
