from tkinter import *
from gamelogic import game_logic


class GameInterface:
    size_grid = -1
    word_grid = []
    words = -1
    words_left = -1
    state = 0
    first = [-1, -1]

    def __init__(self, window: Tk):
        self.win = window
        self.frame = Frame(self.win, width=1280, height=720, background="#3C388D")

    def homeMenu(self):
        self.frame.destroy()
        self.frame = Frame(self.win, width=1280, height=720, background="#3C388D")
        #self.frame.grid_rowconfigure(0, minsize=200)
        #self.frame.grid_rowconfigure(1, minsize=200)
        #self.frame.grid_rowconfigure(3, minsize=200)

        label_1 = Label(self.frame, text="Игра в слова",
                        bg="#36274C",
                        fg="white",
                        font=("Inter", 32),
                        padx="508",
                        pady="40",
                        )
        label_1.grid(row=0, column=0, columnspan=2, pady=20)

        label_2 = Label(self.frame, text="Размер игровой зоны:",
                        bg="#36274C",
                        fg="white",
                        font=("Inter", 18),
                        width="20",
                        pady="25",
                        )
        label_2.grid(row=1, column=0, stick="e", pady=20)

        block = Label(self.frame, text="",
                      bg="#36274C",
                      font=("Inter", 18),
                      width="3",
                      pady="25",
                      )
        block.grid(row=1, column=1, stick="w")

        entry = Entry(self.frame, font=("Inter", 18), width=2)
        entry.grid(row=1, column=1, stick="w")

        btn_1 = Button(self.frame, text="Начать игру",
                       command=lambda: self.inGame(entry.get()),
                       activebackground="grey",
                       font=("Inter", 18),
                       width="20",
                       pady="10"
                       )
        btn_1.grid(row=2, column=0, columnspan=2, pady=20)

        btn_2 = Button(self.frame, text="Правила игры",
                       command=self.rules,
                       activebackground="grey",
                       font=("Inter", 18),
                       width="20",
                       pady="10"
                       )
        btn_2.grid(row=3, column=0, columnspan=2, pady=20)

        btn_3 = Button(self.frame, text="Выход",
                       command=self.win.quit,
                       activebackground="grey",
                       font=("Inter", 18),
                       width="20",
                       pady="10"
                       )
        btn_3.grid(row=4, column=0, columnspan=2, pady=20)
        self.frame.pack()

    def inGame(self, size_grid: str):
        if size_grid.isdigit() == False:
            return

        data = game_logic.startGame(self.size_grid)
        grid = data[0]
        self.words = data[1]
        self.words_left = data[1]
        self.word_grid = data[2]

        self.frame.destroy()
        self.frame = Frame(self.win, width=1280, height=720, background="#3C388D")
        self.frame.grid_rowconfigure(0, pad=70)

        frame_2 = Frame(self.frame, width=650, height=650, background="#36274C")
        frame_2.grid(row=0, column=0, padx=20)

        frame_3 = Frame(self.frame, width=650, height=650, background="#36274C")
        frame_3.grid(row=0, column=0, padx=20)

        self.size_grid = 3 #убрать после!
        buttons = []
        for i in range(self.size_grid):
            temp = []
            for j in range(self.size_grid):
                btn = Button(frame_3, text=grid[i][j], width=3, height=1, pady="4", font=("Inter", 18))
                btn.config(command=lambda x=i, y=j: self.userAnswer(x, y))
                temp.append(btn)
            buttons.append(temp)

        for i in range(self.size_grid):
            for j in range(self.size_grid):
                btn = buttons[i][j]
                btn.grid(row=j, column=i)

        frame_4 = Frame(self.frame, width=300, height=650, background="#3C388D")
        frame_4.grid(row=0, column=1)

        btn_1 = Button(frame_4, text="Переход в меню",
                       command=self.homeMenu,
                       activebackground="grey",
                       font=("Inter", 18),
                       width="20",
                       pady="10"
                       )
        btn_1.place(relx=0, rely=0.002)

        label_2 = Label(frame_4, text=f"Количество оставшихся\nслов: {self.words_left}",
                        bg="#36274C",
                        fg="white",
                        font=("Inter", 18),
                        width=20,
                        height=2,
                        padx="3",
                        pady="5",
                        )
        label_2.place(relx=0, rely=0.15)

        self.frame.pack()

    def userAnswer(self, x: int, y: int):
        print(f"kekw {x}. {y}")
        if self.state == 0:
            self.first = [x, y]
            self.state = 1
        elif self.state == 1:
            flag = 0
            for i in range(0, self.words_left*2, 2):
                if self.word_grid[i][0] == self.first[0] and self.word_grid[i][1] == self.first[1] and self.word_grid[i+1][0] == x and self.word_grid[i+1][1] == y:
                    flag = 1
                    self.word_grid.pop(i)
                    self.word_grid.pop(i)
                    break
            if flag == 1:
                self.words_left -= 1
                self.frame.winfo_children()[2].winfo_children()[1].configure(text=f"Количество оставшихся\nслов: {self.words_left}")
                if self.words_left == 0:
                    self.gameWon()
            self.state = 0

    def gameWon(self):
        win2 = Tk()
        win2["bg"] = "#3C388D"
        win2.title("Статистика")
        win2.geometry("450x500")
        win2.resizable(width=False, height=False)
        label_1 = Label(win2, text="Пройдено!",
                        bg="#36274C",
                        fg="white",
                        font=("Inter", 18),
                        padx="276",
                        pady="10",
                        )
        label_1.pack(pady="20")

        label_1 = Label(win2, text="Статистика:\n\n"
                                   f"Размер игрового поля: {self.size_grid}\n"
                                   f"Количество слов: {self.words}\n"
                                   "Время: 00:00\n",
                        bg="#36274C",
                        fg="white",
                        font=("Inter", 18),
                        width=25,
                        height=5,
                        padx="10",
                        pady="5",
                        anchor="n",
                        )
        label_1.pack()

        btn_1 = Button(win2, text="Начать заново",
                       command=lambda: self.restart(win2),
                       activebackground="grey",
                       font=("Inter", 18),
                       width="20",
                       pady="10"
                       )
        btn_1.pack(pady=20)

        btn_2 = Button(win2, text="Перейти в меню",
                       command=lambda: self.backFromStatistics(win2),
                       activebackground="grey",
                       font=("Inter", 18),
                       width="20",
                       pady="10"
                       )
        btn_2.pack()

    def restart(self, win2: Tk):
        win2.destroy()
        self.inGame(str(self.size_grid))

    def backFromStatistics(self, win2: Tk):
        win2.destroy()
        self.homeMenu()

    def rules(self):
        win2 = Tk()
        win2["bg"] = "#3C388D"
        win2.title("Правила игры")
        win2.geometry("720x470")
        win2.resizable(width=False, height=False)

        label_1 = Label(win2, text="Правила игры",
                        bg="#36274C",
                        fg="white",
                        font=("Inter", 18),
                        padx="276",
                        pady="10",
                        )
        label_1.pack(pady="20")

        label_1 = Label(win2, text="Даётся матрица букв, в которой спрятаны слова.\n\n"
                                   "Размер матрицы принимает значение от 4 до 12,\n"
                                   "само значение задаётся на начальном экране.\n\n"
                                   "Чтобы победить, необходимо найти все слова.\n\n"
                                   "Для нахождения слова нужно нажать на первую\n"
                                   "букву слова, а после на последнюю букву.\n\n"
                                   "Количество оставшихся слов написаны в\n"
                                   "правой части экрана.",
                        bg="#36274C",
                        fg="white",
                        font=("Inter", 18),
                        width=40,
                        height=12,
                        padx="15",
                        pady="10",
                        anchor="n",
                        justify="left"
                        )
        label_1.pack()

    def start(self):
        self.homeMenu()
        self.win.mainloop()
