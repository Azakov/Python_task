from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QApplication, QMessageBox
import sys
import argparse
import os
import cubes_game


class MainWindow(QWidget):
    """Сама форма выбора"""
    def __init__(self, width, level, colors):
        super().__init__()

        self.setWindowTitle("Начало игры ")
        self.setFixedSize(360, 480)
        lab_width = QLabel("Ширина(min = 3,max=100)", self)
        lab_height = QLabel("Высота(min = 3,max=100)", self)
        lab_colors = QLabel("Количество цветов(min = 2,max=8)", self)

        self.width = QLineEdit(str(width), self)
        self.height = QLineEdit(str(level), self)
        self.colors = QLineEdit(str(colors), self)

        start = QPushButton("Старт", self)
        start.clicked.connect(self.start)
        start.setShortcut("ctrl+s")

        scores = QPushButton("Рекорды", self)
        scores.clicked.connect(self.scores)

        grid = QGridLayout(self)

        grid.addWidget(lab_width, 0, 0)
        grid.addWidget(self.width, 0, 1)

        grid.addWidget(lab_height, 1, 0)
        grid.addWidget(self.height, 1, 1)

        grid.addWidget(lab_colors, 2, 0)
        grid.addWidget(self.colors, 2, 1)

        grid.addWidget(start, 3, 0)
        grid.addWidget(scores, 3, 1)

    def start(self):
        """"Функция старта с заданными параметрами"""
        width = int(self.width.text())
        height = int(self.height.text())
        colors = int(self.colors.text())
        if colors > 8:
            colors = 8
        if colors <= 1:
            colors = 2
        if width > 100:
            width = 100
        if height > 100:
            height = 100
        if width < 2:
            width = 3
        if height < 2:
            height = 3

        cubes_game.play(self, width, height, colors)
        self.setVisible(False)

    def scores(self):
        """Показ доски рекордов"""
        try:
            file = open('Scores.txt')
        except IOError:
            QMessageBox.question(self, "Рекорды", "Рекордов нет!", QMessageBox.Ok, QMessageBox.Ok)
        else:
            file.close()
            with open("Scores.txt", 'r') as f:
                list_records = []
                str_records = ""
                for line in f:
                    list_records.append(line)
                for k in list_records:
                    str_records += str(k)
            reply = QMessageBox.question(self, "Result", str_records, QMessageBox.Yes, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                return


def get_args():
    """Парсим аргументы командной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--level", type=int, default=15, help="Высота(по умолчанию 15)")
    parser.add_argument("-w", "--width", type=int, default=15, help="Ширина(по умолчанию 15")
    parser.add_argument("-c", "--colors", type=int, default=4,
                        help="Количество цветов, не больше 8(по умолчанию 4)")
    args = parser.parse_args()
    return args


def main():
    """Начало"""
    app = QApplication(sys.argv)
    args = get_args()
    print(dir(args))
    window = MainWindow(args.width, args.level, args.colors)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
