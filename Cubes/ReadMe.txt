﻿1.Игра кубики с возможностью выбора размеров поля и количества цветов.
Для корректной работы необходимо:
• Python 3.6.0 
• Библиотека PyQt5

2.Автор - Михаил Казаков, студент 2го курса ИЕНИМ, КН-202.

3.Запуск игры - cubes_main.py
Логика поведения игры - cubes_logic.py
Форма игры - cubes_game.py
Тесты - cubes_tests.py
Запуск в консоле(X,Y,Z - размеры поля и кол-во цветов) - 
py -3 cubes_main.py -l X -w Y -c Z

4.В Меню игры можно увидеть окна для ввода параметоров, 
старт - начало игры,рекорды - результаты игры, поставленные вами ранее
Рекорды хранятся в файле Scorces.txt,там же параметры в порядке
[высота,ширина,количество цветов,очки,имя игравшего игрока]
Каждый ход записывается в журнал и таким образом можно пройтись по журналу
неограниченное количество раз.Каждый новый ход преобразует журнал.
Наведя курсор на группу одинаковых кубиков возникает подсветка и
предрасчет очков.Общий результат набранных очков - надпись "Счет",
Результат за ход - надпись "Ход".

5.Меню задается классом MainWindow в файле cubes_main.py,
там же начинается сама игра в методе start;
В cubes_game.py 2 класса:Cell и Game.В Game проходит сам процесс игры
и он обращается к классу Cell при построении поля,к файлу Cubes_logic.py
класс Game обращается уже по ходу игры, в классе mouseReleaseEvent
В классе mouseMoveEvent реализованы функции подсветки и предрасчета.
В методах journal_back и journal_forward реализованы функции журнала,
назад на страницу и вперед соответственно.