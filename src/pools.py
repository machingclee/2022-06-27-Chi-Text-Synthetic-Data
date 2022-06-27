import re
import numpy as np
import chinese_converter as cc
from src import config


class ChiPool:
    def __init__(self, txt_path="chinese_text.txt"):
        self.pool = self.get_chi_char_pool(txt_path=config.chi_text_path)

    def get_chi_char_pool(self, txt_path):
        non_chi_regex = re.compile(r"“|”|！|\s|，|。|；|：|、|…|？|‘|’")
        s = ""
        with open(txt_path, "r", encoding="utf-8") as f:
            for line in f:
                s += line
        pool = re.sub(non_chi_regex, "", s)
        return cc.to_traditional(pool)

    def get_sample(self, smallest_len=3, largest_len=6):
        n_chars = np.random.randint(smallest_len, largest_len+1)
        avaiable_indexes = len(self.pool) - n_chars
        from_index = np.random.randint(0, avaiable_indexes)
        to_index = from_index + n_chars
        return self.pool[from_index:to_index]


class EngPool:
    def __init__(self, txt_path="english_text.txt"):
        self.pool = self.get_eng_char_pool(txt_path=config.eng_text_path)

    def get_eng_char_pool(self, txt_path):
        non_char_regex = re.compile(r"\?|\"|\.|\r\n|\n|\!|,")
        s = ""
        with open(txt_path, "r", encoding="utf-8") as f:
            for line in f:
                s += line
        pool = re.sub(non_char_regex, "", s).split(" ")
        return pool[1:]

    def get_sample(self, smallest_len=2, largest_len=5):
        n_chars = np.random.randint(smallest_len, largest_len+1)
        avaiable_indexes = len(self.pool) - n_chars
        from_index = np.random.randint(0, avaiable_indexes)
        to_index = from_index + n_chars
        return " ".join([w.capitalize() for w in self.pool[from_index:to_index]])


class NumPool:
    def __init__(self):
        self.pool = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    def get_sample(self):
        s = ""
        random_length = 3 + int(np.random.rand()*6)
        for _ in range(random_length):
            index = int(np.random.rand()*8)
            s += self.pool[index]
        return s
