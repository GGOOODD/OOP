from tkinter import *
import random


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Given three collinear points p, q, r, the function checks if


# point q lies on line segment 'pr'
def onSegment(p, q, r):
    if ((q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and
            (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))):
        return True
    return False


def orientation(p, q, r):
    # to find the orientation of an ordered triplet (p,q,r)
    # function returns the following values:
    # 0 : Collinear points
    # 1 : Clockwise points
    # 2 : Counterclockwise

    # See https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/
    # for details of below formula.

    val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
    if (val > 0):

        # Clockwise orientation
        return 1
    elif (val < 0):

        # Counterclockwise orientation
        return 2
    else:

        # Collinear orientation
        return 0


# The main function that returns true if
# the line segment 'p1q1' and 'p2q2' intersect.
def doIntersect(p1, q1, p2, q2):
    # Find the 4 orientations required for
    # the general and special cases
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # General case
    if ((o1 != o2) and (o3 != o4)):
        return True

    # Special Cases

    # p1 , q1 and p2 are collinear and p2 lies on segment p1q1
    if ((o1 == 0) and onSegment(p1, p2, q1)):
        return True

    # p1 , q1 and q2 are collinear and q2 lies on segment p1q1
    if ((o2 == 0) and onSegment(p1, q2, q1)):
        return True

    # p2 , q2 and p1 are collinear and p1 lies on segment p2q2
    if ((o3 == 0) and onSegment(p2, p1, q2)):
        return True

    # p2 , q2 and q1 are collinear and q1 lies on segment p2q2
    if ((o4 == 0) and onSegment(p2, q1, q2)):
        return True

    # If none of the cases
    return False


class GameLogic:
    def startGame(self, size_grid: int):
        words = []
        words_grid = []
        words_left = 0
        grid = []
        for i in range(size_grid):
            temp = []
            for j in range(size_grid):
                temp.append("0")
            grid.append(temp)

        with open("words.txt", encoding="UTF-8") as f:
            lines = f.readlines()

        retries = 0
        exist_num = []
        last_direction = -1
        while retries < 5 or len(words) < size_grid:
            num = random.randint(0, 9282)
            word = lines[num]
            word_len = len(word) - 1
            # print(f"hallo {word_len}")
            # print(f"hallo {word} and {size_grid}")
            if word_len > size_grid:
                continue
            # print(f"bye {words_left}")
            retries += 1
            # 1-7 не слитно ; 8-10 слитно
            merged = 1 # random.randint(1, 10)
            for k in range(5):
                # вправо ; вниз ; вниз-право ; вверх-вправо
                direction = random.randint(0, 3)
                if direction == last_direction:
                    continue
                if merged < 8:
                    if direction == 0:
                        x = random.randint(0, size_grid - word_len)
                        y = random.randint(0, size_grid - 1)
                        flag = 1
                        p1 = Point(x, y)
                        q1 = Point(x + word_len - 1, y)
                        for i in range(len(words_grid)):
                            p2 = Point(words_grid[i][0][0], words_grid[i][0][1])
                            q2 = Point(words_grid[i][1][0], words_grid[i][1][1])
                            if doIntersect(p1, q1, p2, q2):
                                flag = 0
                                break
                        if flag == 1:
                            words.append([word, direction])
                            words_grid.append([[x, y], [x + word_len - 1, y]])
                            words_left += 1
                            exist_num.append(num)
                            last_direction = direction
                            retries = 0
                            break
                    elif direction == 1:
                        x = random.randint(0, size_grid - 1)
                        y = random.randint(0, size_grid - word_len)
                        flag = 1
                        p1 = Point(x, y)
                        q1 = Point(x, y + word_len - 1)
                        for i in range(len(words_grid)):
                            p2 = Point(words_grid[i][0][0], words_grid[i][0][1])
                            q2 = Point(words_grid[i][1][0], words_grid[i][1][1])
                            if doIntersect(p1, q1, p2, q2):
                                flag = 0
                                break
                        if flag == 1:
                            words.append([word, direction])
                            words_grid.append([[x, y], [x, y + word_len - 1]])
                            words_left += 1
                            exist_num.append(num)
                            last_direction = direction
                            retries = 0
                            break
                    elif direction == 2:
                        x = random.randint(0, size_grid - word_len)
                        y = random.randint(0, size_grid - word_len)
                        flag = 1
                        p1 = Point(x, y)
                        q1 = Point(x + word_len - 1, y + word_len - 1)
                        for i in range(len(words_grid)):
                            p2 = Point(words_grid[i][0][0], words_grid[i][0][1])
                            q2 = Point(words_grid[i][1][0], words_grid[i][1][1])
                            if doIntersect(p1, q1, p2, q2):
                                flag = 0
                                break
                        if flag == 1:
                            words.append([word, direction])
                            words_grid.append([[x, y], [x + word_len - 1, y + word_len - 1]])
                            words_left += 1
                            exist_num.append(num)
                            last_direction = direction
                            retries = 0
                            break
                    else:
                        x = random.randint(0, size_grid - word_len)
                        y = random.randint(word_len - 1, size_grid - 1)
                        flag = 1
                        p1 = Point(x, y)
                        q1 = Point(x + word_len - 1, y - (word_len - 1))
                        for i in range(len(words_grid)):
                            p2 = Point(words_grid[i][0][0], words_grid[i][0][1])
                            q2 = Point(words_grid[i][1][0], words_grid[i][1][1])
                            if doIntersect(p1, q1, p2, q2):
                                flag = 0
                                break
                        if flag == 1:
                            words.append([word, direction])
                            words_grid.append([[x, y], [x + word_len - 1, y - (word_len - 1)]])
                            words_left += 1
                            exist_num.append(num)
                            last_direction = direction
                            retries = 0
                            break

        for k in range(len(words)):
            word_grid = words_grid[k]
            word = words[k]
            cnt = 0
            if word[1] == 0:
                for i in range(word_grid[0][0], word_grid[1][0] + 1):
                    grid[i][word_grid[0][1]] = word[0][cnt]
                    cnt += 1
            elif word[1] == 1:
                for i in range(word_grid[0][1], word_grid[1][1] + 1):
                    grid[word_grid[0][0]][i] = word[0][cnt]
                    cnt += 1
            elif word[1] == 2:
                for i in range(max(word_grid[1][0] + 1, word_grid[1][1] + 1) - max(word_grid[0][0], word_grid[0][1])):
                    grid[word_grid[0][0] + i][word_grid[0][1] + i] = word[0][cnt]
                    cnt += 1
            else:
                for i in range(min(word_grid[1][0] - word_grid[0][0] + 1, word_grid[0][1] - word_grid[1][1] + 1)):
                    grid[word_grid[0][0] + i][word_grid[0][1] - i] = word[0][cnt]
                    cnt += 1

        alf = "йцукенгшщзхъфывапролджэячсмитьбю"
        for i in range(size_grid):
            for j in range(size_grid):
                if grid[i][j] == "0":
                    grid[i][j] = alf[random.randint(0, 31)]

        print(words)
        print(words_grid)
        return [grid, words_left, words_grid]


game_logic = GameLogic()
