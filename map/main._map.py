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

        self.x_edit.setText(self.x)
        self.y_edit.setText(self.y)
        self.mashtab.setText(self.masht)

        self.map_request = ['http://static-maps.yandex.ru/1.x/?ll=', self.x, ',', self.y,
                            '&spn=', self.masht, ',', self.masht, '&l=map']
        self.setImageToPixmap()

    def getImage(self):
        self.x = self.x_edit.text().strip()
        self.y = self.y_edit.text().strip()
        self.masht = self.mashtab.text().strip()
        self.map_request = ''.join(['http://static-maps.yandex.ru/1.x/?ll=', self.x, ',',
                                    self.y, '&spn=', self.masht, ',', self.masht, '&l=map'])
        response = requests.get(self.map_request)
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        return 1

    def setImageToPixmap(self):
        is_all_secc = self.getImage()
        print(is_all_secc)
        if is_all_secc:
            self.pixmap = QPixmap(self.map_file)
            self.image.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
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

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyMap()
    ex.show()
    sys.exit(app.exec())
