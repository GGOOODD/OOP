from tkinter import *
from gameinterface import GameInterface


def run():
    win = Tk()
    win["bg"] = "#3C388D"
    win.title("Игра в слова")
    win.geometry("1280x720")
    win.resizable(width=False, height=False)
    game_interface = GameInterface(win)
    game_interface.start()

if __name__ == '__main__':
    run()
