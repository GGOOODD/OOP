from tkinter import *


class GameLogic:
    def startGame(self, size_grid: int):
        word_grid = [[0, 0], [2, 0],
                     [0, 2], [1, 1]]
        words_left = 2
        grid = [["a", "b", "c"],
                ["a", "b", "c"],
                ["a", "b", "c"]]
        return [grid, words_left, word_grid]


game_logic = GameLogic()
