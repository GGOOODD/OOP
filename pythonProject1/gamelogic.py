import random
import time


class Intersect:
    @staticmethod
    def on_segment(p, q, r):
        if ((q["x"] <= max(p["x"], r["x"])) and (q["x"] >= min(p["x"], r["x"])) and
                (q["y"] <= max(p["y"], r["y"])) and (q["y"] >= min(p["y"], r["y"]))):
            return True
        return False

    @staticmethod
    def orientation(p, q, r):
        val = (float(q["y"] - p["y"]) * (r["x"] - q["x"])) - (float(q["x"] - p["x"]) * (r["y"] - q["y"]))
        if val > 0:
            return 1
        elif val < 0:
            return 2
        else:
            return 0

    @staticmethod
    def do_intersect(p1, q1, p2, q2):
        o1 = Intersect.orientation(p1, q1, p2)
        o2 = Intersect.orientation(p1, q1, q2)
        o3 = Intersect.orientation(p2, q2, p1)
        o4 = Intersect.orientation(p2, q2, q1)

        if (o1 != o2) and (o3 != o4):
            return True
        if (o1 == 0) and Intersect.on_segment(p1, p2, q1):
            return True
        if (o2 == 0) and Intersect.on_segment(p1, q2, q1):
            return True
        if (o3 == 0) and Intersect.on_segment(p2, p1, q2):
            return True
        if (o4 == 0) and Intersect.on_segment(p2, q1, q2):
            return True

        return False


class GameLogic:
    start_time: float
    words_left: int

    def generate_words(self, size_grid: int):
        words = []
        words_grid = []
        self.words_left = 0

        with open("words.txt", encoding="UTF-8") as f:
            lines = f.readlines()

        retries = 0
        exist_num = []
        last_direction = -1

        while retries < 25 and len(words) < size_grid:
            num = random.randint(0, 9275)
            word = lines[num].rstrip()
            word_len = len(word)
            if word_len > size_grid:
                continue
            retries += 1
            # 1-4 не слитно ; 5-10 слитно
            merged = random.randint(1, 10)
            if merged < 5:
                for k in range(25):
                    # 0 - вправо ; 1 - вниз ; 2 - вниз-право ; 3 - вверх-вправо
                    dir_num = random.randint(0, 3)
                    if dir_num == last_direction:
                        continue
                    dir_1 = {0: {"x": [0, size_grid - word_len], "y": [0, size_grid - 1]},
                             1: {"x": [0, size_grid - 1], "y": [0, size_grid - word_len]},
                             2: {"x": [0, size_grid - word_len], "y": [0, size_grid - word_len]},
                             3: {"x": [0, size_grid - word_len], "y": [word_len - 1, size_grid - 1]}}
                    x = random.randint(dir_1[dir_num]["x"][0], dir_1[dir_num]["x"][1])
                    y = random.randint(dir_1[dir_num]["y"][0], dir_1[dir_num]["y"][1])
                    dir_2 = {0: {"x": x + word_len - 1, "y": y},
                             1: {"x": x, "y": y + word_len - 1},
                             2: {"x": x + word_len - 1, "y": y + word_len - 1},
                             3: {"x": x + word_len - 1, "y": y - (word_len - 1)}}
                    p1 = {"x": x, "y": y}
                    q1 = dir_2[dir_num]
                    flag = 1
                    for i in range(len(words_grid)):
                        p2 = {"x": words_grid[i][0][0], "y": words_grid[i][0][1]}
                        q2 = {"x": words_grid[i][1][0], "y": words_grid[i][1][1]}
                        if Intersect.do_intersect(p1, q1, p2, q2):
                            flag = 0
                            break
                    if flag == 1:
                        words.append(word)
                        dir_3 = {0: [x + word_len - 1, y],
                                 1: [x, y + word_len - 1],
                                 2: [x + word_len - 1, y + word_len - 1],
                                 3: [x + word_len - 1, y - (word_len - 1)]}
                        words_grid.append([[x, y], dir_3[dir_num], dir_num])
                        self.words_left += 1
                        exist_num.append(num)
                        last_direction = dir_num
                        retries = 0
                        break
            else:
                flag = 0
                for k in range(len(words)):
                    merge_letters = set(word) & set(words[k])
                    if len(merge_letters) == 0:
                        continue
                    for i in range(len(word)):
                        if word[i] not in merge_letters:
                            continue
                        letter = word[i]
                        for j in range(len(words[k])):
                            if words[k][j] != letter:
                                continue
                            dir_1 = {0: {"x": words_grid[k][0][0] + j, "y": words_grid[k][0][1]},
                                     1: {"x": words_grid[k][0][0], "y": words_grid[k][0][1] + j},
                                     2: {"x": words_grid[k][0][0] + j, "y": words_grid[k][0][1] + j},
                                     3: {"x": words_grid[k][0][0] + j, "y": words_grid[k][0][1] - j}}
                            letter_place = dir_1[words_grid[k][2]]
                            for dir_num in range(4):
                                if dir_num == words_grid[k][2]:
                                    continue
                                dir_2 = {0: {"x": letter_place["x"] - i, "y": letter_place["y"]},
                                         1: {"x": letter_place["x"], "y": letter_place["y"] - i},
                                         2: {"x": letter_place["x"] - i, "y": letter_place["y"] - i},
                                         3: {"x": letter_place["x"] - i, "y": letter_place["y"] + i}}
                                p1 = dir_2[dir_num]
                                dir_3 = {0: {"x": p1["x"] + word_len - 1, "y": p1["y"]},
                                         1: {"x": p1["x"], "y": p1["y"] + word_len - 1},
                                         2: {"x": p1["x"] + word_len - 1, "y": p1["y"] + word_len - 1},
                                         3: {"x": p1["x"] + word_len - 1, "y": p1["y"] - (word_len - 1)}}
                                q1 = dir_3[dir_num]
                                if p1["x"] < 0 or p1["y"] < 0 or p1["y"] >= size_grid or q1["x"] >= size_grid or q1["y"] >= size_grid or q1["y"] < 0:
                                    continue
                                flag = 1
                                for w in range(len(words_grid)):
                                    if w == k:
                                        continue
                                    p2 = {"x": words_grid[w][0][0], "y": words_grid[w][0][1]}
                                    q2 = {"x": words_grid[w][1][0], "y": words_grid[w][1][1]}
                                    if Intersect.do_intersect(p1, q1, p2, q2):
                                        flag = 0
                                        break
                                if flag == 1:
                                    words.append(word)
                                    dir_4 = {0: [p1["x"] + word_len - 1, p1["y"]],
                                             1: [p1["x"], p1["y"] + word_len - 1],
                                             2: [p1["x"] + word_len - 1, p1["y"] + word_len - 1],
                                             3: [p1["x"] + word_len - 1, p1["y"] - (word_len - 1)]}
                                    words_grid.append([[p1["x"], p1["y"]], dir_4[dir_num], dir_num])
                                    self.words_left += 1
                                    exist_num.append(num)
                                    last_direction = dir_num
                                    retries = 0
                                    break
                            if flag == 1:
                                break
                        if flag == 1:
                            break
                    if flag == 1:
                        break
        return {"words": words, "words_grid": words_grid}

    def place_words_on_grid(self, size_grid: int, words: list[str], words_grid):
        grid = []
        for i in range(size_grid):
            temp = []
            for j in range(size_grid):
                temp.append("0")
            grid.append(temp)

        for k in range(len(words)):
            word_grid = words_grid[k]
            word = words[k]
            dir_num = words_grid[k][2]
            cnt = 0
            word_dir1 = {0: [word_grid[0][0], word_grid[1][0] + 1],
                         1: [word_grid[0][1], word_grid[1][1] + 1],
                         2: [0, max(word_grid[1][0] + 1, word_grid[1][1] + 1) - max(word_grid[0][0], word_grid[0][1])],
                         3: [0, min(word_grid[1][0] - word_grid[0][0] + 1, word_grid[0][1] - word_grid[1][1] + 1)]}
            for i in range(word_dir1[dir_num][0], word_dir1[dir_num][1]):
                word_dir2 = {0: [i, word_grid[0][1]],
                             1: [word_grid[0][0], i],
                             2: [word_grid[0][0] + i, word_grid[0][1] + i],
                             3: [word_grid[0][0] + i, word_grid[0][1] - i]}
                grid[word_dir2[dir_num][0]][word_dir2[dir_num][1]] = word[cnt]
                cnt += 1

        # пустые места заполняем рандомными буквами
        alf = "йцукенгшщзхъфывапролджэячсмитьбю"
        for i in range(size_grid):
            for j in range(size_grid):
                if grid[i][j] == "0":
                    grid[i][j] = alf[random.randint(0, 31)]

        return grid

    def start_game(self, size_grid: int):
        # выбор слов и их расположения на сетке
        result = self.generate_words(size_grid)
        words = result["words"]
        words_grid = result["words_grid"]

        print(words)
        print(words_grid)

        # располагаем слова на сетке
        grid = self.place_words_on_grid(size_grid, words, words_grid)

        self.start_time = time.time()
        return {"grid": grid, "words_left": self.words_left, "words_grid": words_grid}

    def return_statistic(self):
        return {"time": time.time() - self.start_time, "words_left": self.words_left}


game_logic = GameLogic()
