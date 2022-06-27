from PIL import Image
from PIL import ImageFont, ImageDraw, ImageOps
from glob import glob
import os
import numpy as np
import re
import chinese_converter as cc
import random
from tqdm import tqdm
from src import config
from src.pools import ChiPool, EngPool, NumPool


chi_pool = ChiPool()
eng_pool = EngPool()
num_pool = NumPool()


def _random_angle():
    return int((np.random.randn()-0.5) * 2*config.random_vertical_max_height)


def _random_color():
    color = tuple(np.random.choice(range(256), size=3)) + (255,)
    return color


def _random_verticle_shift():
    return int((np.random.randn()-0.5) * config.random_vertical_max_height)


def _random_font(lang="chi"):
    assert lang in ["chi", "eng"]
    target_fonts = config.font_file_paths
    font_index = int(np.random.rand() * len(target_fonts))
    return target_fonts[font_index]


def _random_sentence_length_font():
    prob = np.random.rand()
    if prob <= 0.5:
        font = _random_font("chi")
        sentence = chi_pool.get_sample()
    elif prob > 0.5 and prob <= 0.75:
        font = _random_font("eng")
        sentence = eng_pool.get_sample()

        prob_2 = np.random.rand()
        if prob_2 < 0.5:
            sentence = sentence.upper()
    else:
        font = _random_font("chi")
        sentence = num_pool.get_sample()

    return sentence, len(sentence), font


def distance(pt1, pt2):
    return np.square(np.sum(np.square(pt1-pt2)))


def generate_cropped_dataset(bg_img_paths):
    bg_img_paths = config.bg_img_paths
    count = 1

    if not os.path.exists(config.training_cropped_text_dir):
        os.makedirs(config.training_cropped_text_dir)
    else:
        cmd = f"rm -rf {config.training_cropped_text_dir}/*"
        os.system(cmd)

    if not os.path.exists(config.training_cropped_bg_dir):
        os.makedirs(config.training_cropped_bg_dir)
    else:
        cmd = f"rm -rf {config.training_cropped_bg_dir}/*"
        os.system(cmd)

    for img in tqdm(bg_img_paths):
        try:
            im = Image.open(img).convert("RGBA")
            im2 = Image.open(img).convert("RGBA")
            im_base = Image.new('RGBA', (im.width, im.height))

            random_color = _random_color()
            random_sentence, sen_len, random_font = _random_sentence_length_font()
            font = ImageFont.truetype(
                random_font, config.font_size, encoding='utf-8')

            txt = Image.new('RGBA', (im.width, im.height))
            d = ImageDraw.Draw(txt)

            remaining_width = max(im.width - sen_len *
                                  (config.font_size+10), 0)
            remaining_height = max(im.height - (config.font_size+10), 0)
            starting_width = int(remaining_width*np.random.rand())
            starting_height = int(remaining_height*np.random.rand())
            starting_pt = (starting_width, starting_height)

            d.text(starting_pt, random_sentence, font=font, stroke_width=0,
                   stroke_fill=(0, 0, 0), fill=random_color)

            im_base = Image.alpha_composite(im_base, im)
            im_base = Image.alpha_composite(im_base, txt)
            im = im_base

            bbox = np.array(txt.getbbox()).reshape(-1, 2)
            enlarged_bbox = bbox.reshape((-1,)) + np.array([-40, -25, 40, 25])
            im = im.crop(enlarged_bbox)
            im2 = im2.crop(enlarged_bbox)

            img_basename = (
                str(count).zfill(5) +
                # font_basename +
                ".png"
            )
            im.save(f"{config.training_cropped_text_dir}/{img_basename}")
            im2.save(f"{config.training_cropped_bg_dir}/{img_basename}")
            count += 1
        except Exception as err:
            pass
