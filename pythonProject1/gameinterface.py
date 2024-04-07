from tkinter import *
from gamelogic import game_logic


class GameInterface:
    def __init__(self, window: Tk):
        self.win = window
        self.frame = Frame(self.win, width=1280, height=720, background="#3C388D")
        self.size_grid = -1
        self.words_grid = []
        self.words = -1
        self.words_left = -1
        self.state = 0
        self.first = [-1, -1]
        self.color = ["#3C388D", "#36274C", "grey", "#f0f0f0", "green"]

    def homeMenu(self):
        self.frame.destroy()
        self.frame = Frame(self.win, width=1280, height=720, background=self.color[0])
        #self.frame.grid_rowconfigure(0, minsize=200)
        #self.frame.grid_rowconfigure(1, minsize=200)
        #self.frame.grid_rowconfigure(3, minsize=200)

        label_1 = Label(self.frame, text="Игра в слова",
                        bg=self.color[1],
                        fg="white",
                        font=("Inter", 32),
                        padx="508",
                        pady="40",
                        )
        label_1.grid(row=0, column=0, columnspan=2, pady=20)

        label_2 = Label(self.frame, text="Размер игровой зоны:",
                        bg=self.color[1],
                        fg="white",
                        font=("Inter", 18),
                        width="20",
                        pady="25",
                        )
        label_2.grid(row=1, column=0, stick="e", pady=20)

        block = Label(self.frame, text="",
                      bg=self.color[1],
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
        if size_grid.isdigit() == False or int(size_grid) < 5 or int(size_grid) > 12:
            return

        self.size_grid = int(size_grid)
        data = game_logic.startGame(self.size_grid)
        grid = data[0]
        self.words = data[1]
        self.words_left = data[1]
        self.words_grid = data[2]

        self.frame.destroy()
        self.frame = Frame(self.win, width=1280, height=720, background=self.color[0])
        self.frame.grid_rowconfigure(0, pad=70)

        frame_2 = Frame(self.frame, width=650, height=650, background=self.color[1])
        frame_2.grid(row=0, column=0, padx=20)

        frame_3 = Frame(self.frame, width=650, height=650, background=self.color[1])
        frame_3.grid(row=0, column=0, padx=20)

        buttons = []
        for i in range(self.size_grid):
            temp = []
            for j in range(self.size_grid):
                btn = Button(frame_3, text=grid[i][j], width=3, height=1, pady="4", font=("Inter", 18),
                             disabledforeground="black", command=lambda x=i, y=j: self.userAnswer(x, y, buttons))
                temp.append(btn)
            buttons.append(temp)

        for i in range(self.size_grid):
            for j in range(self.size_grid):
                btn = buttons[i][j]
                btn.grid(row=j, column=i)

        frame_4 = Frame(self.frame, width=300, height=650, background=self.color[0])
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
                        bg=self.color[1],
                        fg="white",
                        font=("Inter", 18),
                        width=20,
                        height=2,
                        padx="3",
                        pady="5",
                        )
        label_2.place(relx=0, rely=0.15)

        self.frame.pack()

    def changeLinesColor(self, x:int, y:int, buttons: list[list[Button]], color: str):
        for i in range(x, self.size_grid):
            if buttons[i][y]["background"] != "green":
                buttons[i][y].config(background=color, activebackground=color)
        for i in range(y, self.size_grid):
            if buttons[x][i]["background"] != "green":
                buttons[x][i].config(background=color, activebackground=color)
        for i in range(self.size_grid - max(x, y)):
            if buttons[x + i][y + i]["background"] != "green":
                buttons[x + i][y + i].config(background=color, activebackground=color)
        for i in range(min(self.size_grid - x, y + 1)):
            if buttons[x + i][y - i]["background"] != "green":
                buttons[x + i][y - i].config(background=color, activebackground=color)

    def userAnswer(self, x: int, y: int, buttons: list[list[Button]]):
        # print(f"kekw {x}. {y}")
        if self.state == 0:
            self.first = [x, y]
            self.state = 1
            self.changeLinesColor(x, y, buttons, self.color[2])
        elif self.state == 1:
            flag = 0
            self.changeLinesColor(self.first[0], self.first[1], buttons, self.color[3])
            for i in range(0, self.words_left):
                if self.words_grid[i][0][0] == self.first[0] and self.words_grid[i][0][1] == self.first[1] and self.words_grid[i][1][0] == x and self.words_grid[i][1][1] == y:
                    flag = 1
                    self.words_grid.pop(i)
                    break
            if flag == 1:
                if x > self.first[0]:
                    mx = 1
                else:
                    mx = 0
                if y > self.first[1]:
                    my = 1
                elif y == self.first[1]:
                    my = 0
                else:
                    my = -1
                if mx == 1 and my == 1:
                    for i in range(max(x + 1, y + 1) - max(self.first[0], self.first[1])):
                        buttons[self.first[0] + i][self.first[1] + i].config(background="green", activebackground="green")
                elif mx == 1 and my == -1:
                    for i in range(min(x - self.first[0] + 1, self.first[1] - y + 1)):
                        buttons[self.first[0] + i][self.first[1] - i].config(background=self.color[4], activebackground=self.color[4])
                elif mx == 1:
                    for i in range(self.first[0], x + 1):
                        buttons[i][self.first[1]].config(background="green", activebackground="green")
                else:
                    for i in range(self.first[1], y + 1):
                        buttons[self.first[0]][i].config(background="green", activebackground="green")
                self.words_left -= 1
                self.frame.winfo_children()[2].winfo_children()[1].configure(text=f"Количество оставшихся\nслов: {str(self.words_left)}")
                if self.words_left == 0:
                    for i in range(self.size_grid):
                        for j in range(self.size_grid):
                            buttons[i][j].config(state="disabled")
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
