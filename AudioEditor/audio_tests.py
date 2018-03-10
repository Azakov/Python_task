import unittest
import audio_logic
import wave
import scipy.io.wavfile
import io
from scipy import io
import math
import numpy as np


class TestWave:
    """Тестовый wav-файл"""
    def __init__(self):
        music_name = "1test.wav"
        self.data = scipy.io.wavfile.read(music_name)
        self.track_bit = self.data[1]  # data[0] - частота дискретизации
        with wave.open(music_name, 'rb') as self.w:
            self.frame_rate = self.w.getframerate()
            self.frames = self.w.getnframes()
            self.channels = self.w.getnchannels()
            self.width = self.w.getsampwidth()
            self.w.close()


class Tests(unittest.TestCase):
    def test_speed_change(self):
        """Тест на проверку изменения скорости трека"""
        wav = TestWave()
        rate = audio_logic.speed_change(wav.frame_rate, 2)
        self.assertEqual(rate, wav.frame_rate*2)
        rate = audio_logic.speed_change(wav.frame_rate, -2)
        self.assertEqual(rate, wav.frame_rate/2)

    def test_volume_change(self):
        """Тест на проверку изменения громкости трека"""
        wav = TestWave()
        track = audio_logic.volume_change(wav.track_bit, 2)
        self.assertIn(track, wav.track_bit*2)
        track = audio_logic.volume_change(wav.track_bit, -2)
        self.assertIn(track, wav.track_bit//2)

    def test_cut_track_bit(self):
        """Тест на проверку обрезки части трека"""
        wav = TestWave()
        track = audio_logic.cut_track_bit(wav.track_bit, -23, 122, wav.frames)
        self.assertIn(track, wav.track_bit)

    def test_add_track_bit(self):
        """Тест на проверку склеивания двух треков"""
        wav = TestWave()
        half = math.floor(0.01 * 50 * wav.frames)
        track = audio_logic.add_track_bit(wav.track_bit[:half], wav.track_bit[half:])
        self.assertIn(track, wav.track_bit)

    def test_put_track_on_track(self):
        """Тест на проверку наложения треков друг на друга"""
        track = audio_logic.put_track_on_track([[3, 4], [5, 6]], [[1, 9], [4, 4], [8, 8]])
        check = np.array([[4, 13], [9, 10], [8, 8]])
        self.assertIn(track, check)


if __name__ == '__main__':
    unittest.main()
