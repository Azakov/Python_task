import random
from tkinter import *
import time
from tkinter import colorchooser
from tkinter import messagebox
from tkinter.filedialog import *
from tkinter.messagebox import *
from random import randint
from PIL import ImageTk, Image, ImageDraw, ImageOps
from PIL import ImageGrab
import sys


class Application(Frame):
    """Основной класс"""
    def __init__(self, master):
        """Инициализация всех методов создани, а также общие переменные"""
        super().__init__(master)
        self.master = master
        self.tools_thickness = 4
        self.width = 800
        self.height = 600
        self.pack()
        self.create_widgets()
        self.brush_color = "black"
        self.menu_go()
        self.drawn = None
        self.drawn_2 = None
        master.bind('w', self.thickness_plus)
        master.bind('q', self.thickness_minus)

    def create_widgets(self):
        """Создание всех виджетов """
        # Frame ----------------------------------------------------------------------
        self.left_frame = Frame(self)
        self.left_frame.grid(row=0, column=0, columnspan=3, rowspan=3)

        # Canvas ----------------------------------------------------------------------
        self.canvas = Canvas(self, width=self.width,
                             height=self.height, relief=RAISED, borderwidth=5, cursor="pencil", bg="white")
        self.canvas.grid(row=0, column=4, columnspan=30, rowspan=30, pady=1, padx=1, sticky=E + W + S + N)
        self.canvas.rowconfigure(0, weight=1)
        self.canvas.columnconfigure(0, weight=1)
        self.canvas.bind("<Button-1>", self.draw_standart)
        self.canvas.bind("<B1-Motion>", self.draw_standart)


        self.pill  = Image.new("RGB", (self.width, self.height),(255,255,255))
        self.draw_pill = ImageDraw.Draw(self.pill)
        # Clock ----------------------------------------------
        self.label = Label(self.left_frame, font='sans 15')
        self.label.grid(row=0, column=0, rowspan=1)
        self.label.after_idle(self.tick)
        # Widgets ----------------------------------------------
        self.myScale = Scale(
            self.left_frame, orient=HORIZONTAL, length=300, from_=4, to=72, tickinterval=4,
            resolution=4, cursor="hand2",
            command=self.set_thickness)
        self.myScale.grid(row=1, column=0, pady=2, padx=3, sticky=S)

        self.button_color_random = Button(self.left_frame, text="Случайный цвет", command=self.random_color, width=13,
                                          cursor="hand2")
        self.button_color_white = Button(self.left_frame, text="Ластик", width=13, command=self.eraser, cursor="hand2")
        self.button_draw_pencil = Button(self.left_frame, text="Карандаш", width=13,
                                         command=self.pencil, cursor="hand2", bg="#A9A9A9")
        self.button_select_color = Button(self.left_frame, text="Палитра", width=13,
                                          command=self.choose_color, cursor="hand2")
        self.button_spray = Button(self.left_frame, text="Спрей", width=13, command=self.spray, cursor="hand2")
        self.button_deleteAll = Button(self.left_frame, text="Очистить все", width=13,
                                       command=self.delete_all, cursor="hand2")
        self.button_cosmos = Button(self.left_frame, text="Космос", width=13, command=self.cosmos, cursor="hand2")
        self.button_oval = Button(self.left_frame, text="Овал", width=13, command=self.oval, cursor="hand2")
        self.button_line = Button(self.left_frame, text="Линия", width=13, command=self.line, cursor="hand2")
        self.button_rectangle = Button(self.left_frame, text="Прямоугольник", width=13,
                                       command=self.rectangle, cursor="hand2")

        self.button_deleteAll.grid(padx=3, pady=2, row=2, column=0, sticky=NW)
        self.button_color_random.grid(padx=3, pady=2, row=3, column=0, sticky=NW)
        self.button_color_white.grid(padx=3, pady=2, row=4, column=0, sticky=NW)
        self.button_draw_pencil.grid(padx=3, pady=2, row=5, column=0, sticky=NW)
        self.button_select_color.grid(padx=3, pady=2, row=6, column=0, sticky=NW)
        self.button_spray.grid(padx=3, pady=2, row=7, column=0, sticky=NW)
        self.button_cosmos.grid(padx=3, pady=2, row=8, column=0, sticky=NW)
        self.button_oval.grid(padx=3, pady=2, row=9, column=0, sticky=NW)
        self.button_line.grid(padx=3, pady=2, row=10, column=0, sticky=NW)
        self.button_rectangle.grid(padx=3, pady=2, row=11, column=0, sticky=NW)

    # Menu ----------------------------------------------------------------------
    def menu_go(self):
        """Создание вкладки Меню"""
        menu_bar = Menu(self.master)
        self.fileMenu = Menu(self.master, tearoff=0)

        menu_bar.add_cascade(label="Файл", menu=self.fileMenu)
        self.fileMenu.add_command(label="Новый", command=self.new_window)
        self.fileMenu.add_command(label="Открыть", command=self.open_file)
        self.fileMenu.add_command(label="Сохранить", command=self.save_file)
        self.fileMenu.add_command(label="О программе",
                                  command=lambda: showinfo("О программе", "q - уменьшить размер кисти\n"
                                                                          "w - увеличить размер кисти\n"
                                                                          "Размер холста - 1024x600 "))
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Сохранить и выйти", command=self.close_window)
        self.master.config(menu=menu_bar)

    def open_file(self):
        """Открытие файла """
        self.op = askopenfilename(filetypes=[('JPG файлы', '.jpg'), ('BMP файлы', '.bmp'), ('PNG файлы', '.png'),
                                             ('EPS файлы', '.eps'), ('GIF файлы', '.gif'), ('PNM файлы', '.pnm')])
        self.canvas.delete("all")

        self.pill = Image.new("RGB", (self.width, self.height), (255, 255, 255))
        self.draw_pill = ImageDraw.Draw(self.pill)

        self.pilImageOp = Image.open(self.op)
        self.image = ImageTk.PhotoImage(self.pilImageOp)
        self.imagesprite = self.canvas.create_image(0, 0, image=self.image, anchor=NW)

        self.pill = Image.open(self.op)
        self.draw_pill = ImageDraw.Draw(self.pill)

    def save_file(self):
        """Сохранение файла """
        self.a =654
        self.b = 64
        ImageGrab.grab().crop((self.a,self.b , self.a+960, self.b+660)).save("em.jpg")
        self.path = asksaveasfilename(filetypes=[('JPG файлы', '.jpg'), ('BMP файлы', '.bmp'), ('PNG файлы', '.png'),
                                             ('EPS файлы', '.eps'), ('GIF файлы', '.gif'), ('PNM файлы', '.pnm')])
        if not self.path:
            return

        self.pill.save(self.path)

    def close_window(self):
        """Закрытие окна через меню"""
        if askokcancel("Сохранение изображения и выход", "Хотите сохранить и выйти изображение?"):
            self.save_file()
            self.master.destroy()

    def new_window(self):
        """Создание нового изображения через Меню """
        if askyesno("Создание нового изображения", "Хотите ли сохранить текущее изображение?"):
            self.save_file()
            self.pill.save("qeq.jpg", "jpeg")
            self.canvas.delete("all")
            self.pill = Image.new("RGB", (self.width, self.height), (255, 255, 255))
            self.draw_pill = ImageDraw.Draw(self.pill)
        else:
            self.canvas.delete("all")
            self.pill = Image.new("RGB", (self.width, self.height), (255, 255, 255))
            self.draw_pill = ImageDraw.Draw(self.pill)

    # Function_geometry ----------------------------------------------------------------------
    def start_oval(self, event):
        """Стартовая точка для рисования овала """
        self.start = event
        self.drawn = None
        self.drawn_2 = None

    def grow_oval(self, event):
        """Рисование овала"""
        self.canvas = event.widget
        if self.drawn:
            self.canvas.delete(self.drawn)
        object_id = self.canvas.create_oval(self.start.x, self.start.y, event.x, event.y, fill=self.brush_color,
                                            outline=self.brush_color)
        self.drawn = object_id

    def start_line(self, event):
        """Стартовая точка для рисования линии """
        self.start = event
        self.drawn = None


    def grow_line(self, event):
        """Рисование линии"""
        self.canvas = event.widget
        if self.drawn:
            self.canvas.delete(self.drawn)
        object_id = self.canvas.create_line(self.start.x, self.start.y, event.x, event.y, fill=self.brush_color)
        self.drawn = object_id

    def start_rectangle(self, event):
        """Стартовая точка для рисования прямоугольника """
        self.start = event
        self.drawn = None

    def grow_rectangle(self, event):
        """Рисование прямоугольника"""
        self.canvas = event.widget
        if self.drawn:
            self.canvas.delete(self.drawn)
        object_id = self.canvas.create_rectangle(self.start.x, self.start.y, event.x, event.y, fill=self.brush_color,
                                                 outline=self.brush_color)

        self.drawn = object_id

    # Function ----------------------------------------------------------------------
    def set_thickness(self, event):
        """Связь между размером кисти и шкалой размера """
        self.tools_thickness = self.myScale.get()

    def delete_all(self):
        self.canvas.delete("all")
        self.pill = Image.new("RGB", (self.width, self.height), (255, 255, 255))
        self.draw_pill = ImageDraw.Draw(self.pill)

    def draw_standart(self, event):
        """Реализация рисования карандашом """
        self.canvas.create_oval(event.x - self.tools_thickness,
                                event.y - self.tools_thickness,
                                event.x + self.tools_thickness,
                                event.y + self.tools_thickness,
                                fill=self.brush_color, outline=self.brush_color
                                )
        self.draw_pill.ellipse((event.x - self.tools_thickness,
                                event.y - self.tools_thickness,
                                event.x + self.tools_thickness,
                                event.y + self.tools_thickness), fill=self.brush_color, outline=self.brush_color)

    def thickness_plus(self, event):
        """Увеличить размер шкалой """
        if self.tools_thickness < 72:
            self.tools_thickness += 1
            self.myScale.set(self.tools_thickness)

    def thickness_minus(self, event):
        """Уменьшить размер шкалой """
        if 4 < self.tools_thickness:
            self.tools_thickness -= 1
            self.myScale.set(self.tools_thickness)

    def tick(self):
        """Смена времени для часов """
        self.label.after(200, self.tick)
        self.label['text'] = time.strftime('%H:%M:%S')

    def random_color(self):
        """Реализация рандомного цвета """
        r = int(random.random() * 256)
        g = int(random.random() * 256)
        b = int(random.random() * 256)
        rgb = "#%02x%02x%02x" % (r, g, b)
        self.button_color_random["bg"] = rgb
        self.button_color_random["text"] = "Случайный цвет"
        self.button_color_random["fg"] = "white"
        self.brush_color = rgb

    def draw_clear(self, event):
        """Реализация "ластика" """
        self.canvas.create_rectangle(event.x - self.tools_thickness,
                                     event.y - self.tools_thickness,
                                     event.x + self.tools_thickness,
                                     event.y + self.tools_thickness, fill="white", outline="white")
        self.draw_pill.rectangle((event.x - self.tools_thickness,
                                     event.y - self.tools_thickness,
                                     event.x + self.tools_thickness,
                                     event.y + self.tools_thickness) ,fill="white", outline="white")

    # Function_bind_button ----------------------------------------------------------------------
    def eraser(self):
        """Выделение цветом - кнопка "Ластик" """
        self.canvas.bind("<Button-1>", self.draw_clear)
        self.canvas.bind("<B1-Motion>", self.draw_clear)
        self.canvas.config(cursor="target")
        self.button_draw_pencil["bg"] = "#F0F0F0"
        self.button_color_white["bg"] = "#A9A9A9"
        self.button_spray["bg"] = "#F0F0F0"
        self.button_cosmos["bg"] = "#F0F0F0"
        self.button_oval["bg"] = "#F0F0F0"
        self.button_line["bg"] = "#F0F0F0"
        self.button_rectangle["bg"] = "#F0F0F0"

    def pencil(self):
        """Выделение цветом - кнопка "Карандаш" """
        self.canvas.bind("<Button-1>", self.draw_standart)
        self.canvas.bind("<B1-Motion>", self.draw_standart)
        self.canvas.config(cursor="pencil")
        self.button_draw_pencil["bg"] = "#A9A9A9"
        self.button_color_white["bg"] = "#F0F0F0"
        self.button_spray["bg"] = "#F0F0F0"
        self.button_cosmos["bg"] = "#F0F0F0"
        self.button_oval["bg"] = "#F0F0F0"
        self.button_line["bg"] = "#F0F0F0"
        self.button_rectangle["bg"] = "#F0F0F0"

    def spray(self):
        """Выделение цветом - кнопка "Спрей" """
        self.canvas.bind("<Button-1>", self.spray_a)
        self.canvas.bind("<B1-Motion>", self.spray_a)
        self.canvas.config(cursor="spraycan")
        self.button_draw_pencil["bg"] = "#F0F0F0"
        self.button_color_white["bg"] = "#F0F0F0"
        self.button_spray["bg"] = "#A9A9A9"
        self.button_cosmos["bg"] = "#F0F0F0"
        self.button_oval["bg"] = "#F0F0F0"
        self.button_line["bg"] = "#F0F0F0"
        self.button_rectangle["bg"] = "#F0F0F0"

    def cosmos(self):
        """Выделение цветом - кнопка "Космос" """
        self.canvas.bind("<Button-1>", self.space)
        self.canvas.bind("<B1-Motion>", self.space)
        self.canvas.config(cursor="diamond_cross")
        self.button_draw_pencil["bg"] = "#F0F0F0"
        self.button_color_white["bg"] = "#F0F0F0"
        self.button_spray["bg"] = "#F0F0F0"
        self.button_cosmos["bg"] = "#A9A9A9"
        self.button_oval["bg"] = "#F0F0F0"
        self.button_line["bg"] = "#F0F0F0"
        self.button_rectangle["bg"] = "#F0F0F0"

    def oval(self):
        """Выделение цветом - кнопка "Овал" """
        self.canvas.bind('<ButtonPress-1>', self.start_oval)
        self.canvas.bind('<B1-Motion>', self.grow_oval)
        self.canvas.config(cursor="circle")
        self.button_draw_pencil["bg"] = "#F0F0F0"
        self.button_color_white["bg"] = "#F0F0F0"
        self.button_spray["bg"] = "#F0F0F0"
        self.button_cosmos["bg"] = "#F0F0F0"
        self.button_oval["bg"] = "#A9A9A9"
        self.button_line["bg"] = "#F0F0F0"
        self.button_rectangle["bg"] = "#F0F0F0"

    def line(self):
        """Выделение цветом - кнопка "Линия" """
        self.canvas.bind('<ButtonPress-1>', self.start_line)
        self.canvas.bind('<B1-Motion>', self.grow_line)
        self.canvas.config(cursor="top_left_arrow")
        self.button_draw_pencil["bg"] = "#F0F0F0"
        self.button_color_white["bg"] = "#F0F0F0"
        self.button_spray["bg"] = "#F0F0F0"
        self.button_cosmos["bg"] = "#F0F0F0"
        self.button_oval["bg"] = "#F0F0F0"
        self.button_line["bg"] = "#A9A9A9"
        self.button_rectangle["bg"] = "#F0F0F0"

    def rectangle(self):
        """Выделение цветом - кнопка "Прямоугольник" """
        self.canvas.bind('<ButtonPress-1>', self.start_rectangle)
        self.canvas.bind('<B1-Motion>', self.grow_rectangle)
        self.canvas.config(cursor="icon")
        self.button_draw_pencil["bg"] = "#F0F0F0"
        self.button_color_white["bg"] = "#F0F0F0"
        self.button_spray["bg"] = "#F0F0F0"
        self.button_cosmos["bg"] = "#F0F0F0"
        self.button_oval["bg"] = "#F0F0F0"
        self.button_line["bg"] = "#F0F0F0"
        self.button_rectangle["bg"] = "#A9A9A9"
    # Function ----------------------------------------------------------------------

    def choose_color(self):
        """Смена цвета через кнопку "Палитра" """
        self.brush_color = colorchooser.askcolor()[1]
        self.button_select_color["bg"] = self.brush_color

    def spray_a(self, event):
        """Реализация  "Спрея" """
        if self.tools_thickness < 5:
            multiplier = 6
        else:
            multiplier = 2
        x_rand = randint(-self.tools_thickness * multiplier,
                         +self.tools_thickness * multiplier)
        y_rand = randint(-self.tools_thickness * multiplier,
                         +self.tools_thickness * multiplier)

        self.canvas.create_oval(event.x + x_rand, event.y + y_rand,
                                event.x + x_rand + self.tools_thickness, event.y + y_rand + self.tools_thickness,
                                fill=self.brush_color, width=0)
        self.draw_pill.ellipse((event.x + x_rand, event.y + y_rand,
                                event.x + x_rand + self.tools_thickness, event.y + y_rand + self.tools_thickness),
                                fill=self.brush_color)

    def space(self, event):
        """Реализация "космоса" """
        if self.tools_thickness < 5:
            multiplier = 6
        else:
            multiplier = 2
        x_rand = randint(-self.tools_thickness * multiplier,
                         +self.tools_thickness * multiplier)
        y_rand = randint(-self.tools_thickness * multiplier,
                         +self.tools_thickness * multiplier)
        tk_rgb = "#%02x%02x%02x" % (randint(5, 255), randint(10, 150), randint(13, 255))
        self.canvas.create_oval(event.x + x_rand, event.y + y_rand,
                                event.x + self.tools_thickness, event.y + self.tools_thickness, fill=tk_rgb)
        self.draw_pill.ellipse((event.x + x_rand, event.y + y_rand,
                                event.x + self.tools_thickness, event.y + self.tools_thickness), fill=tk_rgb)


root = Tk()
root.title("Растровый редактор изображений")
app = Application(root)


def on_closing():
    """Вызов окна перед закрытием программы """
    if messagebox.askokcancel("Выход", "Вы хотите закрыть программу?"):
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
#root.wm_state('zoomed')
root.mainloop()

#HAHHAHAHAHAHAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHHHHHHHHHHHHHHHHHHHHHHHHAAAAAAAA