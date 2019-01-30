import sys
from PIL import Image
from PyQt5.QtCore import *

from PyQt5.QtGui import *

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PIL.ImageQt import ImageQt


class Drawer(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setAttribute(Qt.WA_StaticContents)
        self.h = 720
        self.w = 1280
        self.Font_Color = Qt.white
        self.myPenWidth = 15
        self.myPenColor = Qt.black
        self.image = QImage(self.w, self.h, QImage.Format_RGB32)
        self.path = QPainterPath()
        self.clearImage()

    def setPenColor(self, newColor):
        self.path = QPainterPath()
        self.myPenColor = newColor

    def setPenWidth(self):
        i, okBtnPressed = QInputDialog.getInt(self, "Размер кисти", "Введите размер кисти", self.myPenWidth, 1, 100, 1)
        if okBtnPressed:
            self.path = QPainterPath()
            self.myPenWidth = i
        self.myCursor()

    def setFont(self):
        color = QColorDialog.getColor()
        self.Font_Color = color
        self.clearImage()

    def clearImage(self):
        self.path = QPainterPath()
        self.image.fill(self.Font_Color)
        self.update()

    def saveImage(self):
        try:
            fname = QFileDialog.getSaveFileName(self, 'Выбор файла', '.')[0]
            self.image.save(fname, fname.split(".")[1].upper())
        except Exception:
            pass

    def loadImage(self):
        self.path = QPainterPath()
        try:
            fname = QFileDialog.getOpenFileName(self, 'Выбор файла', '.')[0]
            self.image = QImage(fname, fname.split(".")[1].upper())
        except Exception:
            pass

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(event.rect(), self.image, self.rect())

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            self.flag = True
            self.path.moveTo(event.pos())

    def mouseMoveEvent(self, event):

        if self.flag:

            self.path.lineTo(event.pos())

            p = QPainter(self.image)

            p.setPen(QPen(self.myPenColor, self.myPenWidth, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

            p.drawPath(self.path)

            p.end()

            self.update()

        else:

            self.path = QPainterPath()

    def sizeHint(self):
        if self.w == 1280 and self.h == 720:
            return QSize(1280, 720)
        return QSize(640, 480)
        self.update()

    def ChangeRes(self):
        if self.w == 1280 and self.h == 720:
            self.w = 640
            self.h = 480
        else:
            self.w = 1280
            self.h = 720
        self.update()
        self.image = QImage(self.w, self.h, QImage.Format_RGB32)
        self.path = QPainterPath()
        self.clearImage()

    def myCursor(self):

        cmap = QPixmap("cursor.png")

        cmap = cmap.scaled(self.myPenWidth + 50 * (1 + self.myPenWidth // 100), self.myPenWidth + 50 * (1 + self.myPenWidth // 100))

        color = self.myPenColor

        self.setCursor(QCursor(cmap))

    def run(self):

        color = QColorDialog.getColor()

        if color.isValid():

            self.setPenColor(color)

            self.path = QPainterPath()

    def filter_invert_color(self):
        x, y = self.image.width(), self.image.height()
        im2 = Image.new("RGB", (x, y), (0, 0, 0))
        pixels2 = im2.load()

        for i in range(x):
            for j in range(y):
                r, g, b = self.image.pixelColor(i, j).getRgb()[:-1]
                pixels2[i, j] = 255 - r, 255 - g, 255 - b
        self.image = ImageQt(im2)
        self.update()
        self.path = QPainterPath()

    def filter_black_and_white(self):
        x, y = self.image.width(), self.image.height()
        im2 = Image.new("RGB", (x, y), (0, 0, 0))
        pixels2 = im2.load()

        for i in range(x):
            for j in range(y):
                r, g, b = self.image.pixelColor(i, j).getRgb()[:-1]
                bw = (r + g + b) // 3
                pixels2[i, j] = bw, bw, bw

        self.image = ImageQt(im2)
        self.update()
        self.path = QPainterPath()

    def filter_left(self):
        x, y = self.image.width(), self.image.height()
        im2 = Image.new("RGB", (x, y), (0, 0, 0))
        pixels2 = im2.load()

        for i in range(x):
            for j in range(y):
                r, g, b = self.image.pixelColor(i, j).getRgb()[:-1]
                pixels2[i, j] = r, g, b
        im2 = im2.transpose(Image.ROTATE_90)
        self.image = ImageQt(im2)
        self.update()

    def filter_right(self):
        x, y = self.image.width(), self.image.height()
        im2 = Image.new("RGB", (x, y), (0, 0, 0))
        pixels2 = im2.load()

        for i in range(x):
            for j in range(y):
                r, g, b = self.image.pixelColor(i, j).getRgb()[:-1]
                pixels2[i, j] = r, g, b
        im2 = im2.transpose(Image.ROTATE_270)
        self.image = ImageQt(im2)
        self.update()


if __name__ == '__main__':

    app = QApplication(sys.argv)

    w = QWidget()
    btnSave = QPushButton("Сохранить")
    btnClear = QPushButton("Очистить полотно")
    btnColorPick = QPushButton("Выбор цвета")
    btnColorFontPick = QPushButton("Выбор фона")
    btnChangeSizeOfPen = QPushButton("Выбор размера кисти")
    btnPenRemover = QPushButton("Ластик")
    btnLoad = QPushButton("Загрузить Файл")
    btnInvert = QPushButton("Инвертировать")
    btnBlack_and_White = QPushButton("Черно-белый")
    btnRight = QPushButton("Повернуть картинку по часовой стрелке")
    btnLeft = QPushButton("Повернуть картинку против часовой стрелки")
    btnChangeRes = QPushButton("Изменить разрешение")
    drawer = Drawer()
    grid = QGridLayout()
    w.setLayout(grid)
    grid.setSpacing(2)


    w.layout().addWidget(btnSave)

    w.layout().addWidget(btnLoad)

    w.layout().addWidget(btnClear)

    w.layout().addWidget(btnChangeRes)

    w.layout().addWidget(btnColorPick)

    w.layout().addWidget(btnChangeSizeOfPen)

    w.layout().addWidget(btnPenRemover)

    w.layout().addWidget(btnColorFontPick)

    w.layout().addWidget(btnInvert)
    w.layout().addWidget(btnBlack_and_White)
    w.layout().addWidget(btnRight)
    w.layout().addWidget(btnLeft)

    w.layout().addWidget(drawer)

    btnSave.clicked.connect(lambda: drawer.saveImage())

    btnClear.clicked.connect(drawer.clearImage)

    btnColorPick.clicked.connect(drawer.run)

    btnColorFontPick.clicked.connect(drawer.setFont)

    btnPenRemover.clicked.connect(lambda: drawer.setPenColor(drawer.Font_Color))

    btnChangeSizeOfPen.clicked.connect(drawer.setPenWidth)

    btnLoad.clicked.connect(drawer.loadImage)

    btnInvert.clicked.connect(drawer.filter_invert_color)
    btnRight.clicked.connect(drawer.filter_right)

    btnLeft.clicked.connect(drawer.filter_left)

    btnChangeRes.clicked.connect(drawer.ChangeRes)
    btnBlack_and_White.clicked.connect(drawer.filter_black_and_white)

    drawer.myCursor()

    w.show()

    sys.exit(app.exec_())