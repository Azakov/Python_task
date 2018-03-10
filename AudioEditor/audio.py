# Python 3.6.0
import wave
import numpy as np
import scipy.io.wavfile
import io
from scipy import io
import argparse
import math
import pyaudio
import os
import pygame
import copy
import sys
import time
import audio_logic
from PyQt5.QtWidgets import QFileDialog, QInputDialog, QLineEdit, QMainWindow, QWidget, QMessageBox

TRACK_1 = []
TRACK_2 = []


class WaveCreate:
    """Создание новой композиции"""
    def __init__(self, music_name, speed, volume, first, end,  code_run):
        global TRACK_1, TRACK_2
        self.classic_rate = 44100
        self.music_name = music_name
        self.data = scipy.io.wavfile.read(music_name)
        self.track_bit = self.data[1]  # data[0] - частота дискретизации
        with wave.open(music_name, 'rb') as self.w:
            self.frame_rate = self.w.getframerate()
            self.frames = self.w.getnframes()
            self.channels = self.w.getnchannels()
            self.width = self.w.getsampwidth()
            self.code_run = code_run
            self.w.close()
        self.frame_rate = audio_logic.speed_change(self.frame_rate, int(speed))
        self.track_bit = audio_logic.volume_change(self.track_bit, int(volume))
        self.track_bit = audio_logic.cut_track_bit(self.track_bit, first, end, self.frames)

        if self.code_run == 0:  # save lonely wav
            self.new_music("change_music.wav")
        elif self.code_run == 1:  # additional track
            TRACK_1 = copy.deepcopy(self.track_bit)
        elif self.code_run == 2:  # and save this
            TRACK_2 = copy.deepcopy(self.track_bit)
            self.track_bit = audio_logic.add_track_bit(TRACK_1, TRACK_2)
            self.frame_rate = self.classic_rate
            self.new_music("glue_music.wav")
        elif self.code_run == 3:  # put track
            TRACK_1 = self.track_bit
        elif self.code_run == 4:  # and save this
            TRACK_2 = self.track_bit
            self.track_bit = audio_logic.put_track_on_track(TRACK_1, TRACK_2)
            self.frame_rate = self.classic_rate*2
            self.new_music("put_music.wav")
        elif self.code_run == 5:  # lonely wav play
            self.play_music(self.music_name)
        elif self.code_run == 6:  # play change wav
            self.new_music("play_change_music.wav")
            self.play_music("play_change_music.wav")
        elif self.code_run == 7:  # stop wav
            self.stop_music()
        elif self.code_run == 8:  # play glue wav
            TRACK_1 = copy.deepcopy(self.track_bit)
        elif self.code_run == 9:  # play glue too
            TRACK_2 = self.track_bit
            self.track_bit = audio_logic.add_track_bit(TRACK_1, TRACK_2)
            self.frame_rate = self.classic_rate
            self.new_music("play_glue_music.wav")
            self.play_music("play_glue_music.wav")
        elif self.code_run == 10:  # play put wav
            TRACK_1 = self.track_bit
        elif self.code_run == 11:  # play put too
            TRACK_2 = self.track_bit
            self.track_bit = audio_logic.put_track_on_track(TRACK_1, TRACK_2)
            self.frame_rate = self.classic_rate * 2
            self.new_music("play_put_music.wav")
            self.play_music("play_put_music.wav")
        elif self.code_run == 12:  # save fragment
            self.new_music("fragment.wav")

    def play_music(self, music_name):
        """Воспроизведение музыки"""
        pygame.init()
        pygame.mixer.music.load(music_name)
        pygame.mixer.music.play()

    def stop_music(self):
        """Остановка воспроизведения"""
        pygame.mixer.music.stop()
        pygame.mixer.music.load("main.wav")
        pygame.mixer.music.play()
        pygame.quit()

    def new_music(self, wave_name):
        """Создание новой композиции как файла"""
        with wave.open(wave_name, 'wb') as new_music:
            new_music.setnchannels(self.channels)
            new_music.setsampwidth(self.width)
            new_music.setframerate(self.frame_rate)
            new_music.writeframes(self.track_bit)
            new_music.close()

if __name__ == '__main__':
    main()
