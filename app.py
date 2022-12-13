import random
from PIL import Image
from PyQt5.QtWidgets import QMainWindow, QListWidget, QApplication, QMenu, QMenuBar, QAction, QFileDialog, QPushButton, QTextBrowser
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen, QBrush
from PyQt5.QtCore import Qt, QPoint
from PyQt5 import QtCore, QtGui
import sys
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QApplication, QComboBox)
import numpy as np


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        title = "Распознаватель букавок"
        top = 200
        left = 200
        width = 720
        height = 360

        self.drawing = False
        self.brushSize = 20
        self.brushColor = Qt.black
        self.lastPoint = QPoint()

        self.image = QImage(300, 300, QImage.Format_RGB32)
        self.image.fill(Qt.white)


        self.text = QTextEdit(self)
        self.text.setGeometry(QtCore.QRect(520, 0, 200, 300))


        self.ListIm = QListWidget()
        self.ListIm.setGeometry(QtCore.QRect(310, 0, 200, 300))


        neural_network = []
        for x in range(4):
            neural_network.append(Window.NeuralNetwork())
        learn_button = QPushButton('Обучить', self)
        learn_button.setGeometry(QtCore.QRect(0, 310, 170, 50))
        learn_button.clicked.connect(lambda: self.learning(neural_network))


        clean_button_Image = QPushButton('Очистить доску', self)
        clean_button_Image.setGeometry(QtCore.QRect(180, 310, 170, 50))
        clean_button_Image.clicked.connect(self.clearDock)


        prediction_button = QPushButton('Распознать', self)
        prediction_button.setGeometry(QtCore.QRect(370, 310, 170, 50))
        prediction_button.clicked.connect(self.save)
        prediction_button.clicked.connect(lambda: self.predict(neural_network))


        clean_button_Text = QPushButton('Очистить текст', self)
        clean_button_Text.setGeometry(QtCore.QRect(550, 310, 170, 50))
        clean_button_Text.clicked.connect(self.clearText)


        self.setWindowTitle(title)
        self.setGeometry(top, left, width, height)

    def print_letter(self, result):
        letters = "ЁАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзиклнопрстуфкцчшщъьэюя"
        self.line.setText(self.line.text() + letters[result])
        return letters[result]

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(0, 0, self.image)

    def save(self):
        self.image.save('res.jpeg')

    def clearDock(self):
        self.image.fill(Qt.white)
        self.update()

    def clearText(self):
        self.text.clear()

    def converting_image_to_array(self, name):
        size = (300, 300)
        image = Image.open("Letters/" + name + ".png").resize(size)
        img_list = list(image.tobytes())
        w, h = image.width, image.height
        result = [[0 for x in range(w)] for y in range(h)]
        i = 0
        r = 0
        y = 0
        while i < img_list.__len__():
            if r != w - 1:
                if img_list[i] == 255 & img_list[i + 1] == 255 & img_list[i + 2] == 255:
                    result[y][r] = 0
                elif img_list[i] == 0 & img_list[i + 1] == 0 & img_list[i + 2] == 0:
                    result[y][r] = 1
                i += 3
                r += 1
            else:
                if img_list[i] == 255 & img_list[i + 1] == 255 & img_list[i + 2] == 255:
                    result[y][r] = 0
                elif img_list[i] == 0 & img_list[i + 1] == 0 & img_list[i + 2] == 0:
                    result[y][r] = 1
                i += 3
                r = 0
                y += 1
        return result

    def learning(self, neural_network):
        data = np.array([
            self.converting_image_to_array("а"),
            self.converting_image_to_array("б"),
            self.converting_image_to_array("в"),
            self.converting_image_to_array("г"),
            self.converting_image_to_array("д"),
            self.converting_image_to_array("е"),
            self.converting_image_to_array("ё"),
            self.converting_image_to_array("ж"),
            self.converting_image_to_array("з"),
            self.converting_image_to_array("и"),
            self.converting_image_to_array("й"),
            self.converting_image_to_array("к"),
            self.converting_image_to_array("л"),
            self.converting_image_to_array("м"),
            self.converting_image_to_array("н"),
            self.converting_image_to_array("о"),
            self.converting_image_to_array("п"),
            self.converting_image_to_array("р"),
            self.converting_image_to_array("с"),
            self.converting_image_to_array("т"),
            self.converting_image_to_array("у"),
            self.converting_image_to_array("ф"),
            self.converting_image_to_array("х"),
            self.converting_image_to_array("ц"),
            self.converting_image_to_array("ч"),
            self.converting_image_to_array("ш"),
            self.converting_image_to_array("щ"),
            self.converting_image_to_array("ъ"),
            self.converting_image_to_array("ы"),
            self.converting_image_to_array("ь"),
            self.converting_image_to_array("э"),
            self.converting_image_to_array("ю"),
            self.converting_image_to_array("я")
        ])
        all_y_trues = 1
        for x in range(4):
            neural_network[x].train(data[x], all_y_trues, 10)

    def predict(self, neural_network):
        image = Image.open("res.jpeg")
        img_list = list(image.tobytes())
        w, h = image.width, image.height
        result = [[0 for x in range(w)] for y in range(h)]
        i = 0
        r = 0
        y = 0
        while i < img_list.__len__():
            if r != w - 1:
                if img_list[i] == 255 & img_list[i + 1] == 255 & img_list[i + 2] == 255:
                    result[y][r] = 0
                elif img_list[i] == 0 & img_list[i + 1] == 0 & img_list[i + 2] == 0:
                    result[y][r] = 1
                i += 3
                r += 1
            else:
                if img_list[i] == 255 & img_list[i + 1] == 255 & img_list[i + 2] == 255:
                    result[y][r] = 0
                elif img_list[i] == 0 & img_list[i + 1] == 0 & img_list[i + 2] == 0:
                    result[y][r] = 1
                i += 3
                r = 0
                y += 1
        #letter = "абвгдеёжзийклнопрстуфкцчшщъыьэюя"
        letter = "абвг"
        for x in range(4):
            self.text.append(letter[x] + " = " + str(neural_network[x].predict(result)) + "\n")
            self.text.append(letter[x] + " = " + str(neural_network[x].predict(self.converting_image_to_array("а"))) + "\n")

    class NeuralNetwork():
        def __init__(self):
            self.synaptic_weights = np.random.random(1)
            self.pred = 0

        def __sigmoid(self, x):
            sc = 1 / (1 + np.exp(-x))
            return sc

        def __sigmoid_derivative(self, x):
            sc = x * (1 - x)
            return sc

        def train(self, training_set_inputs, training_set_outputs, number_of_training_iterations):
            for iteration in range(number_of_training_iterations):
                output = self.think(training_set_inputs)
                error = training_set_outputs - output
                if (error > 0.0001 and error < 0.1) or error == 0:
                    self.pred = output
                adjustment = self.sum_arr(training_set_inputs, error * self.__sigmoid_derivative(output))
                self.synaptic_weights += adjustment

        def think(self, inputs):
            return self.__sigmoid(self.sum_arr(inputs, self.synaptic_weights))

        def predict(self, input):
            if self.pred == self.think(input):
                return 1
            else:
                return 0

        def sum_arr(self, arr, w):
            s = 0
            for i in range(300):
                for j in range(300):
                    s += arr[i][j]*w
            return s


    class Neuron:
        def __init__(self, img):
            self.img = img
            self.w = np.random.rand(900)

        def out(self):
            return self.activation(sum(self.img * self.w))

        def activation(self, out, threshold=0):
            if out > threshold:
                return 1
            else:
                return 0


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
