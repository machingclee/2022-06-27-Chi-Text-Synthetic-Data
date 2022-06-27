import os
import numpy as np
from glob import glob
from tqdm import tqdm
from PIL import Image
from src import config


def generate_mask():
    cropped_txt_mask_dir = config.training_cropped_txt_mask_dir

    if not os.path.exists(cropped_txt_mask_dir):
        os.makedirs(cropped_txt_mask_dir)
    else:
        cmd = f"rm -rf {cropped_txt_mask_dir}/*"
        os.system(cmd)

    cropped_bg_dir = config.training_cropped_bg_dir
    cropped_txt_paths = glob(
        os.path.join(
            config.training_cropped_text_dir,
            "*.png"
        )
    )

    for cropped_txt_path in tqdm(cropped_txt_paths):
        img_basename = os.path.basename(cropped_txt_path)
        bg_img_path = os.path.join(cropped_bg_dir, img_basename)
        cropped_txt_img = np.array(Image.open(cropped_txt_path).convert("L"))
        cropped_bg_img = np.array(Image.open(bg_img_path).convert("L"))

        mask = np.where(
            np.abs(cropped_txt_img - cropped_bg_img) > 0, 255, 0
        ).astype("uint8")

        mask = Image.fromarray(mask)

        if not os.path.exists(cropped_txt_mask_dir):
            os.makedirs(cropped_txt_mask_dir)

        mask.save(os.path.join(cropped_txt_mask_dir, img_basename))
