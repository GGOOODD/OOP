import unittest
from gamelogic import game_logic, Intersect

class TestGameLogic(unittest.TestCase):
    def test_generate_words(self):
        size = 5
        types = (0, 1, 2, 3, 4, 5, 6)
        data = game_logic.generate_words(size, types)
        words = data["words"]
        words_grid = data["words_grid"]
        for i in range(len(words)):
            word_len = len(words[i])
            self.assertLessEqual(word_len, size)
            x1 = words_grid[i][0][0]
            y1 = words_grid[i][0][1]
            x2 = words_grid[i][1][0]
            y2 = words_grid[i][1][1]
            self.assertGreaterEqual(x1, 0)
            self.assertLess(x1, size)
            self.assertGreaterEqual(y1, 0)
            self.assertLess(y1, size)
            self.assertGreaterEqual(x2, 0)
            self.assertLess(x2, size)
            self.assertGreaterEqual(y2, 0)
            self.assertLess(y2, size)

            # 0 - вправо ; 1 - вниз ; 2 - вниз-право ; 3 - вверх-вправо
            direction_number = words_grid[i][2]
            direction_coord = {0: {"x": x1 + word_len - 1, "y": y1},
                               1: {"x": x1, "y": y1 + word_len - 1},
                               2: {"x": x1 + word_len - 1, "y": y1 + word_len - 1},
                               3: {"x": x1 + word_len - 1, "y": y1 - (word_len - 1)}}
            coord_end = {"x": x2, "y": y2}
            test_coord = direction_coord[direction_number]
            self.assertDictEqual(coord_end, test_coord)

    def test_place_words_on_grid(self):
        size = 5
        types = (0, 1, 2, 3, 4, 5, 6)
        data = game_logic.generate_words(size, types)
        words = data["words"]
        words_grid = data["words_grid"]
        # words = ['маша', 'храм', 'цикл', 'ток', 'мина']
        # words_grid = [[[0, 4], [3, 1], 3], [[4, 1], [4, 4], 1], [[0, 0], [3, 0], 0], [[0, 2], [2, 0], 3], [[0, 4], [3, 4], 0]]
        grid = game_logic.place_words_on_grid(size, words, words_grid)
        for i in range(len(words)):
            word = words[i]
            direction_number = words_grid[i][2]
            word_grid = words_grid[i]
            direction_range = {0: [word_grid[0][0], word_grid[1][0] + 1],
                               1: [word_grid[0][1], word_grid[1][1] + 1],
                               2: [0, max(word_grid[1][0] + 1, word_grid[1][1] + 1) - max(word_grid[0][0], word_grid[0][1])],
                               3: [0, min(word_grid[1][0] - word_grid[0][0] + 1, word_grid[0][1] - word_grid[1][1] + 1)]}
            start = direction_range[direction_number][0]
            end = direction_range[direction_number][1]
            cnt = 0
            for j in range(start, end):
                letter_placement = {0: [j, word_grid[0][1]],
                                    1: [word_grid[0][0], j],
                                    2: [word_grid[0][0] + j, word_grid[0][1] + j],
                                    3: [word_grid[0][0] + j, word_grid[0][1] - j]}
                letter_x = letter_placement[direction_number][0]
                letter_y = letter_placement[direction_number][1]
                self.assertEqual(word[cnt], grid[letter_x][letter_y])
                cnt += 1

    def test_do_intersect(self):
        p1 = {"x": 2, "y": 2}
        p2 = {"x": 4, "y": 2}
        p3 = {"x": 4, "y": 4}
        p4 = {"x": 2, "y": 4}
        p5 = {"x": 3, "y": 3}
        self.assertTrue(Intersect.do_intersect(p1, p3, p4, p2))
        self.assertTrue(Intersect.do_intersect(p3, p5, p2, p4))
        self.assertTrue(Intersect.do_intersect(p1, p4, p1, p4))
        self.assertTrue(Intersect.do_intersect(p1, p4, p4, p1))
        self.assertTrue(Intersect.do_intersect(p4, p1, p1, p2))
        self.assertTrue(Intersect.do_intersect(p2, p4, p3, p2))
        self.assertFalse(Intersect.do_intersect(p1, p4, p2, p3))
        self.assertFalse(Intersect.do_intersect(p1, p2, p4, p3))
        self.assertFalse(Intersect.do_intersect(p1, p5, p4, p3))
        self.assertFalse(Intersect.do_intersect(p3, p5, p1, p4))
