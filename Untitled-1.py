# Przed uruchomieniem wpisz w CMD : pip install PyQt5

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
import os
import cv2
import numpy as np

os.system('cls')

class ImageLoaderApp(QWidget):
    def __init__(self):
        super().__init__()

        # Ustawienia okna
        self.setWindowTitle("Aplikacja Schemat")
        self.setGeometry(100, 100, 700, 500)

        # Utwórz widgety
        self.label = QLabel("Kliknij przycisk, aby załadować obraz", self)
        self.button = QPushButton("Załaduj Obraz", self)
        self.button1 = QPushButton("Wyznacz krawędzie", self)

        # Ustawienie labela, aby pokazywał obraz
        self.pixmap = QPixmap()
        self.label.setPixmap(self.pixmap)

        # Podłącz przycisk do funkcji
        self.button.clicked.connect(self.load_image)
        self.button1.clicked.connect(self.apply_filter)

        # Ustawienie rozmiaru labela na 200x200
        self.label.setFixedSize(600, 400)  # Ramka 200x200

        # Utwórz layout i dodaj widgety
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        layout.addWidget(self.button1)  # Przycisk 1

        # Ustaw layout dla głównego okna
        self.setLayout(layout)

    def load_image(self):
        # Otwórz okno dialogowe do wyboru pliku
        file_path, _ = QFileDialog.getOpenFileName(self, "Wybierz obraz", "", "Obrazy (*.png *.jpg *.jpeg *.bmp *.gif)")

        if file_path:
            # Załaduj obraz do QPixmap
            self.pixmap.load(file_path)
            # Wyświetl obraz w QLabel
            self.label.setPixmap(self.pixmap)
            self.label.setScaledContents(True)

    def apply_filter(self):
        if not self.pixmap.isNull():
            # Konwertowanie QPixmap do numpy array
            img = self.pixmap_to_numpy(self.pixmap)
            
            # Zastosowanie filtra Sobela
            sobel_image = self.apply_sobel_filter(img)

            # Konwersja przetworzonego obrazu z powrotem na QPixmap
            sobel_pixmap = self.numpy_to_pixmap(sobel_image)

            # Wyświetlenie przetworzonego obrazu
            self.label.setPixmap(sobel_pixmap)

        else:
            self.label.setText("Załaduj obraz przed zastosowaniem filtra.")

    def pixmap_to_numpy(self, pixmap):
        """
        Funkcja do konwertowania QPixmap na numpy array.
        """
        image = pixmap.toImage()
        image = image.convertToFormat(QImage.Format_RGB888)
        width = image.width()
        height = image.height()
        ptr = image.bits()
        ptr.setsize(image.byteCount())
        arr = np.array(ptr).reshape(height, width, 3)  # Zmieniamy na tablicę (wysokość, szerokość, kanały)
        return arr

    def numpy_to_pixmap(self, img_array):
        """
        Funkcja konwertująca numpy array na QPixmap.
        """
        height, width, channel = img_array.shape
        bytes_per_line = 3 * width
        q_image = QImage(img_array.data, width, height, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(q_image)

    def apply_sobel_filter(self, img, ksize=3):
        """
        Zastosowanie filtra Sobela do obrazu.
        """
        sobel_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=ksize)
        sobel_x = np.abs(sobel_x)

        sobel_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=ksize)
        sobel_y = np.abs(sobel_y)

        sobelxy = cv2.magnitude(sobel_x, sobel_y)
        sobelxy = np.clip(sobelxy, 0, 255).astype(np.uint8)

        return sobelxy


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageLoaderApp()
    window.show()
    sys.exit(app.exec_())