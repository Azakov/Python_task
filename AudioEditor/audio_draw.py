import wave
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math
import scipy.io.wavfile


class WaveDraw:
    """Отрисовка волны wav-файла"""
    def __init__(self, music_name):
        with wave.open(music_name, "r") as wav:
            (self.nchannels, self.sampwidth, self.framerate, self.nframes,
             self.comptype, self.compname) = wav.getparams()
        self.duration = self.nframes / self.framerate
        _w, _h = 800, 200
        self.k = int(self.nframes/_w/32)
        self.DPI = 72
        self.peak = 256 ** self.sampwidth / 2

        data = scipy.io.wavfile.read(music_name)
        samples = data[1]

        plt.figure(1, figsize=(float(_w)/self.DPI, float(_h)/self.DPI), dpi=self.DPI)
        plt.subplots_adjust(wspace=0, hspace=0)

        for n in range(self.nchannels):
            channel = samples[n:]
            channel = channel[0::self.k]
            if self.nchannels == 1:
                channel = channel - self.peak
            axes = plt.subplot(2, 1, n+1, facecolor="k")
            axes.plot(channel, "g")
            axes.yaxis.set_major_formatter(ticker.FuncFormatter(self.format_db))
            plt.grid(True, color="w")
            axes.xaxis.set_major_formatter(ticker.NullFormatter())

        axes.xaxis.set_major_formatter(ticker.FuncFormatter(self.format_time))
        plt.savefig("wave", dpi=self.DPI)

    def format_time(self, x, pos=None):
        """Форматирование времени по номеру сэмпла"""
        progress = int(x / float(self.nframes) * self.duration * self.k)
        mins, secs = divmod(progress, 60)
        hours, mins = divmod(mins, 60)
        out = "%d:%02d" % (mins, secs)
        if hours > 0:
            out = "%d:" % hours
        return out

    def format_db(self, x, pos=None):
        """Форматирование громкости звука по его амплитуде"""
        if pos == 0:
            return ""
        if x == 0:
            return "-inf"
        db = 20 * math.log10(abs(x) / float(self.peak))
        return int(db)
