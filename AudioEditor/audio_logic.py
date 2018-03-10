import math
import numpy as np


def speed_change(frame_rate, change):
    """Изменение скорости воспроизведения"""
    if change > 0:
        return frame_rate * change
    elif change < 0:
        return frame_rate // (change * -1)
    else:
        return


def volume_change(track_bit, change):
    """Изменение громкости звука"""
    if change > 0:
        return track_bit * change
    elif change < 0:
        return track_bit // (change * -1)
    else:
        return


def cut_track_bit(track_bit, percent_start, percent_finish, frames):
    """Вырезка куска трека (в процентах)"""
    if percent_start <= 0:
        percent_start = 0
    if percent_start >= 100:
        percent_start = 99
    if percent_finish >= 100:
        percent_finish = 100
    if percent_finish <= 0:
        percent_finish = 1
    if percent_finish <= percent_start:
        variable = percent_start
        percent_start = percent_finish
        percent_finish = variable
    one_percent = frames * 0.01
    start = math.floor(percent_start * one_percent)
    finish = math.ceil(percent_finish * one_percent)
    return track_bit[start:finish]


def add_track_bit(start_track, finish_track):
    """Сложение двух треков"""
    first = np.array(start_track)
    second = np.array(finish_track)
    return np.concatenate((first, second))


def put_track_on_track(first_track, second_track):
    """Наложение треков друг на друга"""
    first = np.array(first_track)
    second = np.array(second_track)
    nul = [[0, 0]]
    if len(first) > len(second):
        nul = nul * (len(first) - len(second))
        nul_num = np.array(nul)
        second = np.concatenate((second, nul_num))
    elif len(first) < len(second):
        nul = nul * (len(second) - len(first))
        nul_num = np.array(nul)
        first = np.concatenate((first, nul_num))
    return first + second
