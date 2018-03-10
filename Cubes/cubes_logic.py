import random

HEIGHT = 0
WIDTH = 0
scores_per_turn = 0
cell_before_turn = 0
scores_per_turn_copy = 0
cell_before_for_mouse = 0
score = 0
illumination = []


def get_table(height, width, c):
    """Таблица по размеру и заполненная цифрами"""
    global WIDTH, HEIGHT
    WIDTH = width
    HEIGHT = height
    table = []
    for _ in range(height):
        table.append([random.randint(1, c) for _ in range(width)])
    return table


def burst(i, j, table, list_i, list_j):
    """Рекурсивно лопаем клетки"""
    global illumination
    num = table[i][j]
    if num != 0:
        if i < HEIGHT - 1:
            if table[i+1][j] == num:
                table[i][j] = 0
                illumination.append([i, j])
                for k in range(i+1):
                    add_to_list(list_i, k)
                add_to_list(list_j, j)
                burst(i+1, j, table, list_i, list_j)
                table[i+1][j] = 0
                illumination.append([i+1, j])
                add_to_list(list_i, i+1)

        if i > 0:
            if table[i-1][j] == num:
                table[i][j] = 0
                illumination.append([i, j])
                for k in range(i+1):
                    add_to_list(list_i, k)
                add_to_list(list_j, j)
                burst(i-1, j, table, list_i, list_j)
                table[i-1][j] = 0
                illumination.append([i-1, j])
                add_to_list(list_i, i-1)
        if j > 0:
            if table[i][j-1] == num:
                table[i][j] = 0
                illumination.append([i, j])
                for k in range(i+1):
                    add_to_list(list_i, k)
                add_to_list(list_j, j)
                burst(i, j-1, table, list_i, list_j)
                table[i][j-1] = 0
                illumination.append([i, j-1])
                add_to_list(list_j, j-1)
        if j < WIDTH - 1:
            if table[i][j+1] == num:
                table[i][j] = 0
                illumination.append([i, j])
                for k in range(i+1):
                    add_to_list(list_i, k)
                add_to_list(list_j, j)
                burst(i, j+1, table, list_i, list_j)
                table[i][j+1] = 0
                illumination.append([i, j+1])
                add_to_list(list_j, j+1)
    return illumination


def add_to_list(list_add, element):
    """Добавление в лист"""
    for i in list_add:
        if element == i:
            return
    list_add.append(element)


def shift_down(table):
    """Сдвигаем вниз"""
    for _ in range(HEIGHT):
        for i in range(HEIGHT - 1, 0, -1):
            for j in range(WIDTH):
                if table[i][j] == 0:
                    table[i][j] = table[i-1][j]
                    table[i-1][j] = 0


def shift_left(table, list_j):
    """Сдвигаем влево"""
    flag = True
    for _ in range(WIDTH):
        for j in range(WIDTH - 1):
            if table[HEIGHT - 1][j] == 0:
                if flag:
                    for k in range(j, len(table[0])):
                        add_to_list(list_j, k)
                for i in range(HEIGHT):
                    table[i][j] = table[i][j+1]
                    table[i][j+1] = 0


def recount_result(table, flag, cell_before):
    """Подсчёт очков экспоненциально при нажатии"""
    global scores_per_turn_copy, cell_before_turn, scores_per_turn, score
    cell = 0
    if flag:
        cell_before_turn = cell_before
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if table[i][j] == 0:
                cell += 1
    scores_per_turn = (cell-cell_before_turn)**2
    cell_before_turn = cell
    scores_per_turn_copy = scores_per_turn
    cell_before_turn = cell
    return False, scores_per_turn


def recount_result_for_mouse(table, cells_before):
    """Подсчёт очков экспоненциально при движении курсора"""
    cell = 0
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if table[i][j] == 0:
                cell += 1
    result = (cell - cells_before)**2
    return result


def is_there_cell_to_burst(table):
    """Проверка на наличие ходов"""
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if table[i][j] != 0:
                if i != HEIGHT - 1:
                    if table[i+1][j] == table[i][j]:
                        return True
                if i != 0:
                    if table[i-1][j] == table[i][j]:
                        return True
                if j != 0:
                    if table[i][j-1] == table[i][j]:
                        return True
                if j != WIDTH - 1:
                    if table[i][j+1] == table[i][j]:
                        return True
    return False
