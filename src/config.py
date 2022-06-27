import os
from glob import glob

chi_text_path = "txt_files/chinese_text.txt"
eng_text_path = "txt_files/english_text.txt"

random_angle_magnitude = 3
random_vertical_max_height = 100
colors = [(255, 255, 255, 255), (0, 0, 0, 255), (255, 0, 0, 255)]
font_size = 55
font_file_paths = glob("fonts/*.otf") + glob("fonts/*.ttf")
bg_img_paths = glob("bg_without_text/*.png") * 3  # plain bg image without text

training_result_dir = "training_data"

training_cropped_text_dir = f"{training_result_dir}/cropped_text"
training_cropped_bg_dir = f"{training_result_dir}/cropped_background"
training_cropped_txt_mask_dir = f"{training_result_dir}/cropped_text_mask"
