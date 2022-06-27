from src.mask_generation import generate_mask
from src.text_generation import generate_cropped_dataset
from glob import glob


def main():
    generate_cropped_dataset()
    generate_mask()


if __name__ == "__main__":
    main()
