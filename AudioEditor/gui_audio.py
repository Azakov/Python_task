   from PyQt5 import *
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QApplication, QMessageBox,
                             QFileDialog, QCheckBox, QFrame)
from PyQt5.QtCore import Qt
import argparse
import sys
import audio
import re
import pygame
import os
import audio_draw
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPen


class MainWindow(QWidget):
    """Класс отрисовки пользовательского интерфейса"""
    def __init__(self, music_name, speed, volume, first, end, code_run):
        super().__init__()
        self.setWindowTitle("Аудиоредактор")
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)

        self.music_name = music_name
        self.speed = speed
        self.volume = volume
        self.first = first
        self.end = end
        self.code_run = code_run
        self.first_part_of_cut = 0
        self.second_part_of_cut = 100
        self.name_cut = ""

        # QLineEdit -----------------------------------------------------------------------
        self.speed_line = QLineEdit(str(self.speed))
        self.volume_line = QLineEdit(str(self.volume))
        self.first_line = QLineEdit(str(self.first))
        self.end_line = QLineEdit(str(self.end))
        self.speed_line = QLineEdit(str(self.speed))
        self.music_name_line = QLineEdit(str(self.music_name))
        self.glue_first_line = QLineEdit("")
        self.glue_second_line = QLineEdit("")
        self.put_first_line = QLineEdit("")
        self.put_second_line = QLineEdit("")

        # QPushButton -----------------------------------------------------------------------

        self.start_lonely_button = QPushButton("Воспроизведение и изображение")
        self.stop_lonely_button = QPushButton("Стоп")

        self.start_change_button = QPushButton("Воспроизведение изменений")
        self.save_change_button = QPushButton("Сохранить")
        self.stop_change_button = QPushButton("Стоп")

        self.start_glue_button = QPushButton("Воспроизведение склейки")
        self.save_glue_button = QPushButton("Сохранить")
        self.stop_glue_button = QPushButton("Стоп")

        self.start_put_button = QPushButton("Воспроизведение наложения")
        self.save_put_button = QPushButton("Сохранить")
        self.stop_put_button = QPushButton("Стоп")

        self.choose_track_button = QPushButton("Выбрать")
        self.choose_glue_first_button = QPushButton("Выбрать")
        self.choose_glue_second_button = QPushButton("Выбрать")
        self.choose_put_first_button = QPushButton("Выбрать")
        self.choose_put_second_button = QPushButton("Выбрать")
        self.go_cut = QPushButton("Редактировать фрагмент")
        # QLabel -----------------------------------------------------------------------

        self.music_name_label = QLabel("Выбереть трек")
        self.speed_label = QLabel("Изменить скорость  %s в" % self.music_name_line.text())
        self.volume_label = QLabel("Изменить звук %s в" % self.music_name_line.text())
        self.track_cut_1_label = QLabel("Обрезать %s с " % self.music_name_line.text())
        self.track_cut_2_label = QLabel("% до ")
        self.glue_label = QLabel("Склеить трек")
        self.together_label = QLabel("с треком")
        self.put_label = QLabel("Наложить трек")
        self.on_label = QLabel("на трек")
        self.wall = QLabel("-"*200)
        self.plot = QLabel()
        self.part_of_cut_label = QLabel()
        self.name_track = QLabel()
        # -----------------------------------------------------------------------

        self.check_box = QCheckBox("Обрезать трек")

        # QGridLayout -----------------------------------------------------------------------

        self.grid = QGridLayout(self)
        self.frame = QFrame()
        self.frame.setStyleSheet("background-color: rgb(200, 255, 0)")
        self.grid.addWidget(self.frame, 1, 0, 4, 5)
        self.frame = QFrame()
        self.frame.setStyleSheet("background-color: rgb(0, 255, 200)")
        self.grid.addWidget(self.frame, 5, 0, 2, 6)
        self.frame = QFrame()
        self.frame.setStyleSheet("background-color: rgb(133, 255, 102)")
        self.grid.addWidget(self.frame, 7, 0, 2, 6)
        # 1 -----------------------------------------------------------------------
        widgets = [self.music_name_label, self.music_name_line, self.choose_track_button,
                   self.start_lonely_button, self.stop_lonely_button]

        self.grid_add_widget(1, widgets)
        self.start_lonely_button.clicked.connect(self.play_wav_lonely)
        self.stop_lonely_button.clicked.connect(self.stop_play_music_lonely)
        self.choose_track_button.clicked.connect(self.file_to_speed_vol_cut)

        # 2 -----------------------------------------------------------------------
        widgets = [self.speed_label, self.speed_line, self.volume_label, self.volume_line]

        self.grid_add_widget(2, widgets)
        # 3 -----------------------------------------------------------------------
        widgets = [self.track_cut_1_label, self.first_line, self.track_cut_2_label, self.end_line, self.check_box]

        self.widgets_3 = widgets.copy()
        self.widgets_3.pop()
        self.check_box.toggle()
        self.check_box.stateChanged.connect(self.change_check)
        self.grid_add_widget(3, widgets)
        # 4 -----------------------------------------------------------------------
        widgets = [self.start_change_button, self.stop_change_button, self.save_change_button]

        self.save_change_button.clicked.connect(self.save_wav_change)
        self.start_change_button.clicked.connect(self.play_change_wav)
        self.stop_change_button.clicked.connect(self.stop_play_music_change)
        self.grid_add_widget(4, widgets)
        # 5 -----------------------------------------------------------------------
        widgets = [self.glue_label, self.glue_first_line, self.choose_glue_first_button, self.together_label,
                   self.glue_second_line, self.choose_glue_second_button]

        self.choose_glue_first_button.clicked.connect(self.file_to_glue_1)
        self.choose_glue_second_button.clicked.connect(self.file_to_glue_2)
        self.grid_add_widget(5, widgets)
        # 6 -----------------------------------------------------------------------
        widgets = [self.start_glue_button, self.stop_glue_button, self.save_glue_button]

        self.grid_add_widget(6, widgets)
        self.save_glue_button.clicked.connect(self.save_glue)
        self.start_glue_button.clicked.connect(self.play_glue_wav)
        self.stop_glue_button.clicked.connect(self.stop_play_music_glue)
        # 7 -----------------------------------------------------------------------
        widgets = [self.put_label, self.put_first_line, self.choose_put_first_button,
                   self.on_label, self.put_second_line, self.choose_put_second_button]

        self.choose_put_first_button.clicked.connect(self.file_to_put_1)
        self.choose_put_second_button.clicked.connect(self.file_to_put_2)
        self.grid_add_widget(7, widgets)
        # 8 -----------------------------------------------------------------------
        widgets = [self.start_put_button, self.stop_put_button, self.save_put_button]

        self.save_put_button.clicked.connect(self.save_put)
        self.start_put_button.clicked.connect(self.play_put_wav)
        self.stop_put_button.clicked.connect(self.stop_play_music_put)
        self.grid_add_widget(8, widgets)
        self.grid.addWidget(self.wall, 9, 0, 1, 7)
        self.setLayout(self.grid)
    # -----------------------------------------------------------------------

    def grid_add_widget(self, position, widgets):
        """Прикрепление виджетов"""
        i = 0
        for w in widgets:
            self.grid.addWidget(w, position, i)
            i += 1

    def change_check(self, check):
        """Проверка на поле "Обрезать трек" """
        for w in self.widgets_3:
            if check == Qt.Checked:
                w.setDisabled(False)
            else:
                w.setDisabled(True)
                self.first_line.setText("0")
                self.end_line.setText("100")

    # play -----------------------------------------------------------------------
    def play_wav_lonely(self):
        """Воспроизведение выбраной композиции"""
        music_name = self.music_name_line.text()
        self.code_run = 5
        try:
            audio.WaveCreate(music_name, 1, 1, 0, 100, self.code_run)
            self.show_plot(music_name)
        except:
            QMessageBox.question(self, "Ошибка!", "Некорректно введенные данные или \nостановите воспроизведение \n"
                                                  "и повторите операцию", QMessageBox.Ok, QMessageBox.Ok)

    def play_change_wav(self):
        """Воспроизведение измененной композиции"""
        music_name = self.music_name_line.text()
        speed = int(self.speed_line.text())
        volume = int(self.volume_line.text())
        first = int(self.first_line.text())
        end = int(self.end_line.text())
        self.code_run = 6
        try:
            audio.WaveCreate(music_name, speed, volume, first, end, self.code_run)
        except:
            QMessageBox.question(self, "Ошибка!", "Некорректно введенные данные или \nостановите воспроизведение \n"
                                                  "и повторите операцию", QMessageBox.Ok, QMessageBox.Ok)

    def play_glue_wav(self):
        """Воспроизведение склееной композиции"""
        music_name_1 = self.glue_first_line.text()
        music_name_2 = self.glue_second_line.text()
        self.code_run = 8
        try:
            audio.WaveCreate(music_name_1, 1, 1, 0, 100, self.code_run)
            self.code_run = 9
            audio.WaveCreate(music_name_2, 1, 1, 0, 100, self.code_run)
        except:
            QMessageBox.question(self, "Ошибка!", "Некорректно введенные данные или \nостановите воспроизведение \n"
                                                  "и повторите операцию", QMessageBox.Ok, QMessageBox.Ok)

    def play_put_wav(self):
        """Воспроизведение наложенной композиции"""
        music_name_1 = self.put_first_line.text()
        music_name_2 = self.put_second_line.text()
        try:
            self.code_run = 10
            audio.WaveCreate(music_name_1, 1, 1, 0, 100, self.code_run)
            self.code_run = 11
            audio.WaveCreate(music_name_2, 1, 1, 0, 100, self.code_run)
        except:
            QMessageBox.question(self, "Ошибка!", "Некорректно введенные данные или \nостановите воспроизведение \n"
                                                  "и повторите операцию", QMessageBox.Ok, QMessageBox.Ok)

    # stop -----------------------------------------------------------------------
    def stop_play_music_lonely(self):
        """Остановка выбраной композиции"""
        music_name = self.music_name_line.text()
        self.code_run = 7
        try:
            audio.WaveCreate(music_name, 1, 1, 0, 100, self.code_run)

        except:
            QMessageBox.question(self, "Ошибка!", "Нет трека для остановки воспроизведения",
                                 QMessageBox.Ok, QMessageBox.Ok)

    def stop_play_music_change(self):
        """Остановка измененной композиции"""
        music_name = "play_change_music.wav"
        self.code_run = 7
        try:
            audio.WaveCreate(music_name, 1, 1, 0, 100, self.code_run)
        except:
            QMessageBox.question(self, "Ошибка!",  "Нет трека для остановки воспроизведения",
                                 QMessageBox.Ok, QMessageBox.Ok)

    def stop_play_music_glue(self):
        """Остановка склееной композиции"""
        music_name = "play_glue_music.wav"
        self.code_run = 7
        try:
            audio.WaveCreate(music_name, 1, 1, 0, 100, self.code_run)
        except:
            QMessageBox.question(self, "Ошибка!",  "Нет трека для остановки воспроизведения",
                                 QMessageBox.Ok, QMessageBox.Ok)

    def stop_play_music_put(self):
        """Остановка наложенной композиции"""
        music_name = "play_put_music.wav"
        self.code_run = 7
        try:
            audio.WaveCreate(music_name, 1, 1, 0, 100, self.code_run)
        except:
            QMessageBox.question(self, "Ошибка!",  "Нет трека для остановки воспроизведения",
                                 QMessageBox.Ok, QMessageBox.Ok)
    # save -----------------------------------------------------------------------

    def save_wav_change(self):
        """Сохранение измененной композиции"""
        music_name = self.music_name_line.text()
        speed = int(self.speed_line.text())
        volume = int(self.volume_line.text())
        first = int(self.first_line.text())
        end = int(self.end_line.text())
        self.code_run = 0
        try:
            audio.WaveCreate(music_name, speed, volume, first, end, self.code_run)
            QMessageBox.question(self, "Сохранение", "Сохранено как change_music.wav", QMessageBox.Ok, QMessageBox.Ok)
        except:
            QMessageBox.question(self, "Ошибка!", "Некорректно введенные данные", QMessageBox.Ok, QMessageBox.Ok)

    def save_glue(self):
        """Сохранение склееной композиции"""
        music_name_1 = self.glue_first_line.text()
        music_name_2 = self.glue_second_line.text()
        self.code_run = 1
        try:
            audio.WaveCreate(music_name_1, 1, 1, 0, 100, self.code_run)
            self.code_run = 2
            audio.WaveCreate(music_name_2, 1, 1, 0, 100, self.code_run)
            QMessageBox.question(self, "Сохранение", "Сохранено как glue_music.wav", QMessageBox.Ok, QMessageBox.Ok)
        except:
            QMessageBox.question(self, "Ошибка!", "Некорректно введенные данные", QMessageBox.Ok, QMessageBox.Ok)

    def save_put(self):
        """Сохранение наложенной композиции"""
        music_name_1 = self.put_first_line.text()
        music_name_2 = self.put_second_line.text()
        self.code_run = 3
        try:
            audio.WaveCreate(music_name_1, 1, 1, 0, 100, self.code_run)
            self.code_run = 4
            audio.WaveCreate(music_name_2, 1, 1, 0, 100, self.code_run)
            QMessageBox.question(self, "Сохранение", "Сохранено как put_music.wav", QMessageBox.Ok, QMessageBox.Ok)
        except:
            QMessageBox.question(self, "Ошибка!", "Некорректно введенные данные", QMessageBox.Ok, QMessageBox.Ok)

    # file work -----------------------------------------------------------------------
    def file_to_speed_vol_cut(self):
        """Изменеие текста в надписях в соответствии с названием одиночного трека"""
        self.music_name_line.setText(self.get_file_name("main.wav"))
        self.speed_label.setText("Изменить скорость %s в" % self.music_name_line.text())
        self.volume_label.setText("Изменить звук %s в" % self.music_name_line.text())
        self.track_cut_1_label.setText("Обрезать %s с " % self.music_name_line.text())

    def file_to_glue_1(self):
        """Получение названия трека для первого поля склейки"""
        self.glue_first_line.setText(self.get_file_name(""))

    def file_to_glue_2(self):
        """Получение названия трека для второго поля склейки"""
        self.glue_second_line.setText(self.get_file_name(""))

    def file_to_put_1(self):
        """Получение названия трека для первого поля наложения"""
        self.put_first_line.setText(self.get_file_name(""))

    def file_to_put_2(self):
        """Получение названия трека для второго поля наложения"""
        self.put_second_line.setText(self.get_file_name(""))

    def get_file_name(self, start_name):
        """Получение названия трека"""
        fname = QFileDialog.getOpenFileName(self, 'Open file', start_name, "*.wav")
        if fname[0] == '':
            return
        name_music = re.findall(r'/(\w*\d*\s*.wav)', fname[0])
        return name_music[0]
    # draw wav and fragments work -----------------------------------------------------------------------

    def show_plot(self, music_name):
        """Показ интерактивного изображения трека"""
        audio_draw.WaveDraw(music_name)
        pixmap = QPixmap("wave.png")
        self.plot.setPixmap(pixmap)
        self.grid.addWidget(self.plot, 10, 0, 4, 0)
        self.name_track.setText(music_name)
        self.grid.addWidget(self.name_track, 10, 6)
        self.name_cut = music_name
        if self.grid.indexOf(self.go_cut) < 0:
            self.grid.addWidget(self.go_cut, 12, 6)
            self.go_cut.clicked.connect(self.fragments_redactor)

    def fragments_redactor(self):
        """Сохранение выбранного фрагмента"""
        try:
            audio.WaveCreate(self.name_cut, 1, 1, self.first_part_of_cut, self.second_part_of_cut, 12)
            QMessageBox.question(self, "Сохранение фрагмента", "Сохранено как fragment.wav", QMessageBox.Ok,
                                 QMessageBox.Ok)
        except:
            QMessageBox.question(self, "Ошибка!", "Остановите воспроизведение и повторите операцию", QMessageBox.Ok,
                                 QMessageBox.Ok)
    def mousePressEvent(self, event):
        """События нажатия мыши"""
        if event.x() >= 141 and event.x() <= 706 and event.y() <= 482 and event.y() >= 329:
            self.first_part_of_cut = int((event.x() - 141) * 100 / 565)
            self.part_of_cut_label.setText("Вырезать кусок от %s %%" % str(self.first_part_of_cut))
            self.grid.addWidget(self.part_of_cut_label, 11, 6)

    def mouseReleaseEvent(self, event):
        """События отжатия мыши"""
        if event.x() >= 141 and event.x() <= 706 and event.y() <= 482 and event.y() >= 329:
            self.second_part_of_cut = int((event.x() - 141) * 100 / 565)
            if self.second_part_of_cut < self.first_part_of_cut:
                var = self.second_part_of_cut
                self.second_part_of_cut = self.first_part_of_cut
                self.first_part_of_cut = var
            self.part_of_cut_label.setText("Вырезать кусок от %d %% до %d %%" % (self.first_part_of_cut,
                                                                                 self.second_part_of_cut))
            # -----------------------------------------------------------------------


def get_args():
    """Парсим аргументы командной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--track", default='main.wav', help="Выберете трек! (по умолчанию main.wav) ")
    parser.add_argument("-s", "--speed", type=float, default=1, help="Изменение скорости воспроизведения "
                                                                     "(по умолчанию 0)")
    parser.add_argument("-v", "--volume", type=float, default=1,
                        help="Изменение громкости звука (по умолчанию 0)")
    parser.add_argument("-f", "--first", type=int, default=0, help="Начало среза композиции (по умолчанию 0)")
    parser.add_argument("-e", "--end", type=int, default=100, help="Конец среза композиции(по умолчанию 100)")
    args = parser.parse_args()
    return args


def main():
    """Запуск программые с аргументами"""
    app = QApplication(sys.argv)
    args = get_args()
    window = MainWindow(args.track, args.speed, args.volume, args.first, args.end,  0)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
