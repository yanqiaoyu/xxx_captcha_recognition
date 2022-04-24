import argparse
import cv2, os
from utils import operate_img, noise_unsome_piexl
import pytesseract

ImageName = ''
ImageDir = 'pic'

def parse_arg():
    global ImageName
    parser = argparse.ArgumentParser(description='Process ADS captach')
    parser.add_argument('-n', '--name', type=str,help='specified the captcha name', dest='captcha_name', required = True)
    args = parser.parse_args()
    ImageName = args.captcha_name

def Binarization():
    global ImageName
    img = cv2.imread(f"./{ImageDir}/{ImageName}")
    img2 = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img2 = cv2.inRange(img2, lowerb=160, upperb=255)
    cv2.imwrite(f"./{ImageDir}/{ImageName}", img2)

def NoiseReduction():
    img = cv2.imread(f"./{ImageDir}/{ImageName}")
    _, img2 = cv2.threshold(img, 160, 255, cv2.THRESH_BINARY)
    img3 = operate_img(img2, 4)
    img4 = noise_unsome_piexl(img3)

    cv2.imwrite(f"./{ImageDir}/{ImageName}", img4)

def Recognition():
    result = pytesseract.image_to_string(f"./{ImageDir}/{ImageName}", lang="ads").replace(' ', '')[0:4]
    print(result)

if __name__ == "__main__":
    parse_arg()
    Binarization()
    NoiseReduction()
    Recognition()
    
