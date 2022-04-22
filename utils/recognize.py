import argparse
import cv2
import os
from utils.recognize_utils import operate_img, noise_unsome_piexl
import pytesseract

image_path = './pic/'
image_name = ''


def Recognize(name):
    global image_name
    image_name = name
    Binarization()
    NoiseReduction()
    Recognition()


def Binarization():

    img = cv2.imread(f"{image_path}{image_name}")
    img2 = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img2 = cv2.inRange(img2, lowerb=160, upperb=255)
    cv2.imwrite(f"{image_path}{image_name}", img2)


def NoiseReduction():
    img = cv2.imread(f"{image_path}{image_name}")
    _, img2 = cv2.threshold(img, 160, 255, cv2.THRESH_BINARY)
    img3 = operate_img(img2, 4)
    img4 = noise_unsome_piexl(img3)

    cv2.imwrite(f"{image_path}{image_name}", img4)


def Recognition():
    result = pytesseract.image_to_string(
        f"{image_path}{image_name}", lang="ads").replace(' ', '')[0:4]
    print(result)


if __name__ == "__main__":
    Binarization()
    NoiseReduction()
    Recognition()
