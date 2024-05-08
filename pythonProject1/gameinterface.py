from tkinter import *
from gamelogic import game_logic


class GameInterface:
    def __init__(self, window: Tk):
        self.win = window
        self.size_grid = -1
        self.words_grid = []
        self.words_left = -1
        self.types = ()
        self.first = [-1, -1]
        self.color = ["#3C388D", "#36274C", "grey",
                      "#f0f0f0", "green", "#006400"]
        Frame(self.win, width=1280, height=720, background=self.color[0])

    def home_menu(self):
        self.win.winfo_children()[0].destroy()
        frame = Frame(self.win, width=1280, height=720,
                      background=self.color[0])

        label_1 = Label(frame, text="Игра в слова",
                        bg=self.color[1], fg="white", font=("Inter", 32),
                        padx="508", pady="40",
                        )
        label_1.grid(row=0, column=0, columnspan=2, pady=20)

        frame1 = Frame(frame, background=self.color[0])
        frame1.grid(row=1, column=0, pady=20, stick="e", padx="10")

        label_2 = Label(frame1, text="Размер игровой зоны:",
                        bg=self.color[1], fg="white", font=("Inter", 18),
                        width="20", pady="23",
                        )
        label_2.grid(row=0, column=0, stick="e", pady=20)

        block = Label(frame1, text="",
                      bg=self.color[1], font=("Inter", 18),
                      width="3", pady="23",
                      )
        block.grid(row=0, column=1, stick="w")

        entry = Entry(frame1, font=("Inter", 18), width=2)
        entry.grid(row=0, column=1, stick="w")

        frame2 = Frame(frame, background=self.color[1])
        frame2.grid(row=1, column=1, stick="w", padx="10")

        types = ["Животные", "Биология", "Физика", "Растения",
                 "Профессии", "Спорт", "Технологии"]
        types_var = StringVar(value=types)
        listbox = Listbox(frame2, listvariable=types_var, selectmode=MULTIPLE,
                          font=("Inter", 18), width=10, height=7)
        listbox.select_set(0, 6)
        listbox.pack()

        btn_1 = Button(frame, text="Начать игру",
                       command=lambda: self.in_game(entry.get(),
                                                    listbox.curselection()),
                       activebackground="grey", font=("Inter", 18),
                       width="25", padx="66", pady="10"
                       )
        btn_1.grid(row=2, column=0, columnspan=2, pady=20)

        btn_2 = Button(frame, text="Правила игры",
                       command=self.rules,
                       activebackground="grey", font=("Inter", 18),
                       width="25", padx="66", pady="10"
                       )
        btn_2.grid(row=3, column=0, columnspan=2)

        btn_3 = Button(frame, text="Выход",
                       command=self.win.quit,
                       activebackground="grey", font=("Inter", 18),
                       width="25", padx="66", pady="10"
                       )
        btn_3.grid(row=4, column=0, columnspan=2, pady=20)
        frame.pack()

    def in_game(self, size_grid: str, types: tuple):
        if (size_grid.isdigit() is False or int(size_grid) < 5 or
                int(size_grid) > 12 or len(types) == 0):
            return

        self.size_grid = int(size_grid)
        self.types = types
        data = game_logic.start_game(self.size_grid, types)
        grid = data["grid"]
        self.words_left = data["words_left"]
        self.words_grid = data["words_grid"]

        self.win.winfo_children()[0].destroy()
        frame = Frame(self.win, width=1280, height=720,
                      background=self.color[0])
        frame.grid_rowconfigure(0, pad=70)

        frame_2 = Frame(frame, width=650, height=650, background=self.color[1])
        frame_2.grid(row=0, column=0, padx=20)

        frame_3 = Frame(frame, width=650, height=650, background=self.color[1])
        frame_3.grid(row=0, column=0, padx=20)

        buttons = []
        for i in range(self.size_grid):
            temp = []
            for j in range(self.size_grid):
                btn = Button(frame_3, text=grid[i][j], width=3, height=1,
                             pady="4", font=("Inter", 18),
                             disabledforeground="black",
                             command=lambda x=i, y=j:
                             self.user_answer(x, y, buttons, frame))
                temp.append(btn)
            buttons.append(temp)

        for i in range(self.size_grid):
            for j in range(self.size_grid):
                btn = buttons[i][j]
                btn.grid(row=j, column=i)

        frame_4 = Frame(frame, width=300, height=650, background=self.color[0])
        frame_4.grid(row=0, column=1)

        btn_1 = Button(frame_4, text="Переход в меню",
                       command=self.home_menu,
                       activebackground="grey", font=("Inter", 18),
                       width="20", pady="10"
                       )
        btn_1.place(relx=0, rely=0.002)

        label_2 = Label(frame_4, text=f"Количество оставшихся\nслов: "
                                      f"{self.words_left}",
                        bg=self.color[1], fg="white", font=("Inter", 18),
                        width=20, height=2, padx="3", pady="5",
                        )
        label_2.place(relx=0, rely=0.15)

        frame.pack()

    def change_lines_color(self, x: int, y: int, buttons: list[list[Button]],
                           color: str, green_color: str):
        for i in range(x, self.size_grid):
            if (buttons[i][y]["background"] != self.color[4] and
                    buttons[i][y]["background"] != self.color[5]):
                buttons[i][y].config(background=color, activebackground=color)
            else:
                buttons[i][y].config(background=green_color,
                                     activebackground=green_color)
        for i in range(y, self.size_grid):
            if (buttons[x][i]["background"] != self.color[4] and
                    buttons[x][i]["background"] != self.color[5]):
                buttons[x][i].config(background=color, activebackground=color)
            else:
                buttons[x][i].config(background=green_color,
                                     activebackground=green_color)
        for i in range(self.size_grid - max(x, y)):
            if (buttons[x + i][y + i]["background"] != self.color[4] and
                    buttons[x + i][y + i]["background"] != self.color[5]):
                buttons[x + i][y + i].config(background=color,
                                             activebackground=color)
            else:
                buttons[x + i][y + i].config(background=green_color,
                                             activebackground=green_color)
        for i in range(min(self.size_grid - x, y + 1)):
            if (buttons[x + i][y - i]["background"] != self.color[4] and
                    buttons[x + i][y - i]["background"] != self.color[5]):
                buttons[x + i][y - i].config(background=color,
                                             activebackground=color)
            else:
                buttons[x + i][y - i].config(background=green_color,
                                             activebackground=green_color)

    def user_answer(self, x: int, y: int, buttons: list[list[Button]],
                    frame: Frame):
        if self.first == [-1, -1]:
            self.first = [x, y]
            self.change_lines_color(x, y, buttons, self.color[2], self.color[5])
        else:
            flag = 0
            self.change_lines_color(self.first[0], self.first[1], buttons,
                                    self.color[3], self.color[4])
            for i in range(0, self.words_left):
                if (self.words_grid[i][0][0] == self.first[0] and
                        self.words_grid[i][0][1] == self.first[1] and
                        self.words_grid[i][1][0] == x and
                        self.words_grid[i][1][1] == y):
                    flag = 1
                    dir_num = self.words_grid[i][2]
                    self.words_grid.pop(i)
                    break
            if flag == 1:
                if dir_num == 2:
                    for i in range(max(x + 1, y + 1) -
                                   max(self.first[0], self.first[1])):
                        (buttons[self.first[0] + i][self.first[1] + i]
                         .config(background=self.color[4],
                                 activebackground=self.color[4]))
                elif dir_num == 3:
                    for i in range(min(x - self.first[0] + 1,
                                       self.first[1] - y + 1)):
                        (buttons[self.first[0] + i][self.first[1] - i]
                         .config(background=self.color[4],
                                 activebackground=self.color[4]))
                elif dir_num == 0:
                    for i in range(self.first[0], x + 1):
                        (buttons[i][self.first[1]]
                         .config(background=self.color[4],
                                 activebackground=self.color[4]))
                else:
                    for i in range(self.first[1], y + 1):
                        (buttons[self.first[0]][i]
                         .config(background=self.color[4],
                                 activebackground=self.color[4]))
                self.words_left -= 1
                (frame.winfo_children()[2].winfo_children()[1]
                 .configure(text=f"Количество оставшихся\nслов: "
                                 f"{str(self.words_left)}"))
                if self.words_left == 0:
                    for i in range(self.size_grid):
                        for j in range(self.size_grid):
                            buttons[i][j].config(state="disabled")
                    self.game_won()
            self.first = [-1, -1]

    def game_won(self):
        win2 = Tk()
        win2["bg"] = "#3C388D"
        win2.title("Статистика")
        win2.geometry("450x620")
        win2.resizable(width=False, height=False)
        label_1 = Label(win2, text="Пройдено!",
                        bg="#36274C", fg="white", font=("Inter", 18),
                        padx="276", pady="10",
                        )
        label_1.pack(pady=20)

        data = game_logic.return_statistic()
        mins = int(data["time"] / 60)
        secs = int(data["time"] % 60)
        types_name = {0: "животные", 1: "биология", 2: "физика", 3: "растения",
                      4: "профессии", 5: "спорт", 6: "технологии"}
        types_text = ""
        text_i = 0
        for i in self.types:
            if text_i != 0:
                if text_i % 2 == 1:
                    types_text += ", "
                else:
                    types_text += "\n"
            types_text += types_name[i]
            text_i += 1
        types_text += "\n"

        label_1 = Label(win2, text="Статистика\n\n"
                                   f"Размер игрового поля: {self.size_grid}\n"
                                   "Выбранные категории слов:\n"
                                   f"{types_text}"
                                   f"Количество слов: {data['words_left']}\n"
                                   f"Время: {mins}:{secs}\n",
                        bg="#36274C", fg="white", font=("Inter", 18),
                        width=23, height=10, padx="5", pady="5", anchor="n",
                        )
        label_1.pack(pady=30)

        btn_1 = Button(win2, text="Начать заново",
                       command=lambda: self.restart_from_statistics(win2),
                       activebackground="grey", font=("Inter", 18),
                       width="23", padx="5", pady="10"
                       )
        btn_1.pack()

        btn_2 = Button(win2, text="Перейти в меню",
                       command=lambda: self.back_from_statistics(win2),
                       activebackground="grey", font=("Inter", 18),
                       width="23", padx="5", pady="10"
                       )
        btn_2.pack(pady=30)

    def restart_from_statistics(self, win2: Tk):
        win2.destroy()
        self.in_game(str(self.size_grid), self.types)

    def back_from_statistics(self, win2: Tk):
        win2.destroy()
        self.home_menu()

    def rules(self):
        win2 = Tk()
        win2["bg"] = "#3C388D"
        win2.title("Правила игры")
        win2.geometry("720x580")
        win2.resizable(width=False, height=False)

        label_1 = Label(win2, text="Правила игры",
                        bg="#36274C", fg="white", font=("Inter", 18),
                        padx="280", pady="10",
                        )
        label_1.pack(pady="20")

        label_1 = Label(win2,
                        text="Даётся матрица букв, в которой спрятаны слова.\n"
                             "\nРазмер матрицы принимает значение от 5 до 12,\n"
                             "само значение задаётся в главном меню.\n"
                             "\nКатегории слов выбираются в главном меню,\n"
                             "по умолчанию выбраны все категории.\n"
                             "\nЧтобы победить, необходимо найти все слова.\n"
                             "Слова могут пересекаться между собой.\n"
                             "\nДля нахождения слова нужно нажать на первую\n"
                             "букву слова, а после на последнюю букву.\n"
                             "\nКоличество оставшихся слов написаны в\n"
                             "правой части игрового окна.",
                        bg="#36274C", fg="white", font=("Inter", 18),
                        width=40, height=16, padx="15", pady="10",
                        anchor="n", justify="left"
                        )
        label_1.pack()

    def start(self):
        self.home_menu()
        self.win.mainloop()
