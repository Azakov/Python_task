import cubes_logic
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QInputDialog, QLineEdit, QGraphicsView
from PyQt5.QtGui import QColor
import copy
import math


class Game(QMainWindow):
    """Само окно"""
    def __init__(self, window, width, height, colors):
        """Инициализация всех переменных и объектов"""
        super().__init__(window)
        self.setWindowTitle("Кубики")
        self.setMouseTracking(True)
        self.size = 20

        self.journal = []
        self.journal_history = []
        self.journal_copy = []
        self.journal_position = 0

        self.scores_per_turn_list = [0]
        self.scores_per_turn_list_copy = [0]

        self.cells_per_turn = []
        self.cells_per_turn_copy = []
        self.cells_per_turn_sum = 0
        self.scores_per_mouse_move = 0

        self.colors = {0: QColor(255, 255, 255), 1: QColor(255, 0, 0), 2: QColor(0, 255, 0),
                       3: QColor(0, 0, 255), 4: QColor(255, 255, 0),
                       5: QColor(255, 0, 255), 6: QColor(0, 255, 255),
                       7: QColor(128, 0, 128), 8: QColor(0, 128, 128)}

        self.result_check_change = 0

        self.scores_per_turn = 0
        self.scores_per_mouse_move = 0

        self.result_sum = 0
        self.flag = False
        self.height = height
        self.width = width
        self.num_colors = colors
        self.list_i = []
        self.list_j = []

        self.res_per_turn_lab = QLabel("Ход:" + str(self.scores_per_mouse_move), self)
        self.res_per_turn_lab.setGeometry(80, self.size*height, 700, 20)

        self.res_lab = QLabel("Счёт: "+str(self.result_sum), self)
        self.res_lab.setGeometry(0, height*self.size, 700, 20)

        self.back = QPushButton("Назад", self)
        self.back.setGeometry(0, height*self.size + 20, 50, 20)
        self.back.clicked.connect(self.journal_back)

        self.forward = QPushButton("Вперед", self)
        self.forward.setGeometry(50, height * self.size + 20, 50, 20)
        self.forward.clicked.connect(self.journal_forward)

        self.setFixedSize(width*self.size, height*self.size+40)

        self.table = cubes_logic.get_table(height, width, self.num_colors)
        self.field = self.get_field()

    # Mouse Functions-----------------------------------------------------------------

    def mouseMoveEvent(self, event):
        """События движения курсора"""
        list_i_event = []
        list_j_event = []

        table_event = copy.deepcopy(self.table)

        i = event.y() // self.size
        j = event.x() // self.size

        if i > self.height - 1 or j > self.width - 1:
            return
        colors = {0: QColor(255, 255, 255), -1: QColor(150, 0, 0), -2: QColor(0, 150, 0),
                  -3: QColor(0, 0, 150), -4: QColor(150, 150, 0),
                  -5: QColor(150, 0, 150), -6: QColor(0, 150, 150),
                  -7: QColor(75, 0, 75), -8: QColor(0, 75, 75)}

        illumination = cubes_logic.burst(i, j, table_event, list_i_event, list_j_event)
        illumination_2 = []

        for k in illumination:
            if k not in illumination_2:
                illumination_2.append(k)

        cubes_logic.shift_down(table_event)
        cubes_logic.shift_left(table_event, list_j_event)

        self.refresh_colors()
        for p in illumination_2:
            self.field[p[0]][p[1]].set_color(colors[self.table[p[0]][p[1]]*-1])
        cubes_logic.illumination.clear()

        self.scores_per_mouse_move = cubes_logic.recount_result_for_mouse(table_event, self.cells_per_turn_sum)
        self.res_per_turn_lab.setText("Ход: " + str(self.scores_per_mouse_move))

    def mouseReleaseEvent(self, event):
        """События отжатия мыши"""
        if self.journal_position == 0:
            self.journal.clear()
            self.journal.append(copy.deepcopy(self.table))

        i = event.y() // self.size
        j = event.x() // self.size
        if i > self.height - 1 or j > self.width - 1:
            return

        self.journal_copy = copy.deepcopy(self.journal)
        self.result_check_change = self.result_sum

        cubes_logic.burst(i, j, self.table, self.list_i, self.list_j)
        cubes_logic.shift_down(self.table)
        cubes_logic.shift_left(self.table, self.list_j)

        self.flag, self.scores_per_turn = cubes_logic.recount_result(self.table, self.flag, self.cells_per_turn_sum)

        self.result_sum += self.scores_per_turn
        self.res_lab.setText("Счёт: " + str(self.result_sum))
        self.res_per_turn_lab.setText("Ход: " + str(self.scores_per_mouse_move))

        self.change_colors()

        self.event_by_click_if_result_change()

        if not cubes_logic.is_there_cell_to_burst(self.table):
            self.return_results()
        self.list_i.clear()
        self.list_j.clear()

    # Journal ------------------------------------------------------------------------------------------

    def journal_back(self):
        """Журнал на страницу назад"""
        if self.journal_position == 0:
            return
        self.journal.pop()
        self.journal_position -= 1
        self.table = self.journal[self.journal_position]
        self.refresh_colors()

        self.flag = True
        self.cells_per_turn.pop()
        self.cells_per_turn_sum -= int(math.sqrt(self.scores_per_turn_list[len(self.scores_per_turn_list) - 1]))

        self.result_sum -= self.scores_per_turn_list[len(self.scores_per_turn_list) - 1]
        self.scores_per_turn_list.pop()
        self.scores_per_turn = 0

        self.res_lab.setText("Счёт: " + str(self.result_sum))
        self.res_per_turn_lab.setText("Ход: 0")

    def journal_forward(self):
        """Журнал на страницу вперед"""
        if ((self.journal_position == 0) and (len(self.journal) == 0)) or\
                (self.journal_position == len(self.journal_history) - 1):
            return

        self.journal_position += 1
        self.table = copy.deepcopy(self.journal_history[self.journal_position])
        self.journal.append(copy.deepcopy(self.table))
        self.refresh_colors()

        self.result_sum += self.scores_per_turn_list_copy[len(self.scores_per_turn_list)]
        self.scores_per_turn_list.append(self.scores_per_turn_list_copy[len(self.scores_per_turn_list)])

        self.cells_per_turn_sum += self.cells_per_turn_copy[len(self.cells_per_turn)]
        self.cells_per_turn.append(self.cells_per_turn_copy[len(self.cells_per_turn)])

        self.res_lab.setText("Счёт: " + str(self.result_sum))
        self.res_per_turn_lab.setText("Ход: 0")

    # Operation with field and finite result-----------------------------------------------------------

    def get_field(self):
        """Поле клеток"""
        field = []
        for i in range(self.height):
            lst = []
            for j in range(self.width):
                lst.append(Cell(self, i, j, self.colors[self.table[i][j]]))
            field.append(lst)
        return field

    def refresh_colors(self):
        """Смена цвета клетки при использовании журнала(визуально)"""
        for i in range(self.height):
            for j in range(self.width):
                if self.table[i][j] == 0 and self.field[i][j].color == self.colors[0]:
                    continue
                self.field[i][j].set_color(self.colors[self.table[i][j]])

    def change_colors(self):
        """Смена цвета у клетки при нажатии мыши(визуально)"""
        for i in self.list_i:
            for j in self.list_j:
                if self.table[i][j] == 0 and self.field[i][j].color == self.colors[0]:
                    continue
                self.field[i][j].set_color(self.colors[self.table[i][j]])

    def event_by_click_if_result_change(self):
        """События при изменения результата"""
        if self.result_check_change != self.result_sum and self.scores_per_turn != 0:
            self.journal_position += 1
            self.journal_copy.append(copy.deepcopy(self.table))
            self.journal = copy.deepcopy(self.journal_copy)
            self.journal_history = copy.deepcopy(self.journal)

            self.scores_per_turn_list.append(self.scores_per_turn)
            self.scores_per_turn_list_copy = copy.deepcopy(self.scores_per_turn_list)

            self.cells_per_turn_sum += int(math.sqrt(self.scores_per_turn_list[len(self.scores_per_turn_list) - 1]))
            self.cells_per_turn.append(int(math.sqrt(self.scores_per_turn_list[len(self.scores_per_turn_list) - 1])))
            self.cells_per_turn_copy = copy.deepcopy(self.cells_per_turn)

    def return_results(self):
        """Вывод результата"""
        text, game_name = QInputDialog.getText(self, "Конец", "Результат:" + str(self.result_sum)
                                               + "\nВведите имя:", QLineEdit.Normal, "Player")
        if game_name is False:
            exit(0)
        else:
            if text != '':
                name = text

        with open("Scores.txt", 'a') as f:

            f.write("%s: ширина - %d, высота - %d, цветов - %d, результат - %d \n" % (name, self.width, self.height,
                                                                                      self.num_colors, self.result_sum))
            f.close()
            exit(0)


class Cell(QLabel):
    """Создание кубика на клетке"""
    def __init__(self, window, i, j, color):
        super().__init__(window)
        self.size = 20
        self.color = color
        self.setGeometry(self.size*j, self.size*i, self.size, self.size)
        self.set_color(color)
        self.setMouseTracking(True)

    def set_color(self, color):
        """Устанавливаем цвет"""
        self.setStyleSheet("QLabel { background-color: %s }" % color.name())


def play(window, width, height, colors):
    """Запуск приложения"""
    game = Game(window, width, height, colors)
    game.show()
