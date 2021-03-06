import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel
from PyQt5 import uic
from PyQt5.QtCore import Qt


class MyMap(QWidget):
    def __init__(self):
        super().__init__()
        self.x, self.y, self.masht = '37.530887', '55.703118', '0.002'

        uic.loadUi('map_designe.ui', self)
        self.pushButton.clicked.connect(self.setImageToPixmap)
        self.setWindowTitle('Map_app')
        self.vid = 'map'

        self.x_edit.setText(self.x)
        self.y_edit.setText(self.y)
        self.mashtab.setText(self.masht)

        self.map_request_str = ''
        self.map_request = ['http://static-maps.yandex.ru/1.x/?ll=', self.x, ',',
                            self.y, '&spn=', self.masht, ',', self.masht, '&l=', self.vid]
        self.setImageToPixmap()
        self.setSelfFocus()

    def getImage(self):
        self.x = self.x_edit.text()
        self.y = self.y_edit.text()
        self.masht = self.mashtab.text()
        if self.layer.currentIndex() == 0:
            self.vid = 'sat'
        if self.layer.currentIndex() == 1:
            self.vid = 'map'
        if self.layer.currentIndex() == 2:
            self.vid = 'skl'
        self.map_request = ['http://static-maps.yandex.ru/1.x/?ll=', self.x, ',',
                            self.y, '&spn=', self.masht, ',', self.masht, '&l=', self.vid]
        self.map_request_str = ''.join(self.map_request)
        response = requests.get(self.map_request_str)
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        return 1

    def setImageToPixmap(self):
        is_all_secc = self.getImage()
        if is_all_secc:
            self.pixmap = QPixmap(self.map_file)
            self.image.setPixmap(self.pixmap)
        self.setSelfFocus()

    def keyPressEvent(self, event):
        a = event
        if event.key() == Qt.Key_PageUp:
            try:
                self.mashtab.setText(str(float(self.mashtab.text()) * 2))
                self.setImageToPixmap()
            except FloatingPointError as e:
                print(e)
        elif event.key() == Qt.Key_PageDown:
            try:
                self.mashtab.setText(str(float(self.mashtab.text()) / 2))
                self.setImageToPixmap()
            except FloatingPointError as e:
                print(e)
        elif event.key() == Qt.Key_Up:
            print(2)
            try:
                self.y_edit.setText(str(float(self.y_edit.text()) - 2 * float(self.mashtab.text())))
                self.setImageToPixmap()
            except FloatingPointError as e:
                print(e)
        elif event.key() == Qt.Key_Down:
            print(1)
            try:
                self.y_edit.setText(str(float(self.y_edit.text()) + 2 * float(self.mashtab.text())))
                self.setImageToPixmap()
            except FloatingPointError as e:
                print(e)
        elif event.key() == Qt.Key_Right:
            try:
                self.x_edit.setText(str(float(self.x_edit.text()) + 2 * float(self.mashtab.text())))
                self.setImageToPixmap()
            except FloatingPointError as e:
                print(e)
        elif event.key() == Qt.Key_Left:
            try:
                self.x_edit.setText(str(float(self.x_edit.text()) - 2 * float(self.mashtab.text())))
                self.setImageToPixmap()
            except FloatingPointError as e:
                print(e)

    def setSelfFocus(self):
        self.setFocusPolicy(Qt.StrongFocus)

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyMap()
    ex.show()
    sys.exit(app.exec())
