import os
import requests
import cv2
from PIL import Image
import shutil
import pytesseract

URL = 'https://***'
path_1 = "pic"
img_cnt = 1

#获取验证码
def GetReCapthcha():
    if not os.path.exists(path_1):
        os.mkdir(path_1)

    #获取img_cnt张验证码，并保存下来
    for count in range(img_cnt):
        session = requests.session()
        pig = session.request("GET", URL, headers={}, verify=False)
        with open('./' + path_1 + '/' + f'{count+1}.png', 'wb') as file:
            file.write(pig.content)

#二值化处理
def Binarization():
    os.chdir("./"+path_1)
    for count in range(img_cnt):
        img = cv2.imread(f"{count+1}.png")
        img2 = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img2 = cv2.inRange(img2, lowerb=160, upperb=255)
        cv2.imwrite(f'{count+1}.png', img2)
    os.chdir("../")

def operate_img(img,k):
    w,h,s = img.shape
    # 从高度开始遍历
    for _w in range(w):
        # 遍历宽度
        for _h in range(h):
            if _h != 0 and _w != 0 and _w < w-1 and _h < h-1:
                if calculate_noise_count(img, _w, _h) < k:
                    img.itemset((_w,_h,0),255)
                    img.itemset((_w, _h,1), 255)
                    img.itemset((_w, _h,2), 255)

    return img

# 计算邻域非白色个数
def calculate_noise_count(img_obj, w, h):
    """
    计算邻域非白色的个数
    Args:
        img_obj: img obj
        w: width
        h: height
    Returns:
        count (int)
    """
    count = 0
    width, height,s = img_obj.shape
    for _w_ in [w - 1, w, w + 1]:
        for _h_ in [h - 1, h, h + 1]:
            if _w_ > width - 1:
                continue
            if _h_ > height - 1:
                continue
            if _w_ == w and _h_ == h:
                continue
            if (img_obj[_w_, _h_,0] < 233) or (img_obj[_w_, _h_,1] < 233) or (img_obj[_w_, _h_,2] < 233):
                count += 1
    return count

# 邻域非同色降噪
def noise_unsome_piexl(img):
    '''
    查找像素点上下左右相邻点的颜色，如果是非白色的非像素点颜色，则填充为白色
    :param img:
    :return:
    '''
    # print(img.shape)
    w, h, s = img.shape
    for _w in range(w):
        for _h in range(h):
            if _h != 0 and _w != 0 and _w < w - 1 and _h < h - 1:# 剔除顶点、底点
                center_color = img[_w, _h] # 当前坐标颜色
                # print(center_color)
                top_color = img[_w, _h + 1]  
                bottom_color = img[_w, _h - 1] 
                left_color = img[_w - 1, _h]  
                right_color = img[_w + 1, _h]  
                cnt = 0
                if all(top_color == center_color):
                    cnt += 1
                if all(bottom_color == center_color):
                    cnt += 1
                if all(left_color == center_color):
                    cnt += 1
                if all(right_color == center_color):
                    cnt += 1
                if cnt < 1:
                    img.itemset((_w, _h, 0), 255)
                    img.itemset((_w, _h, 1), 255)
                    img.itemset((_w, _h, 2), 255)
    return img

#去噪点
def NoiseReduction():
    os.chdir("./"+path_1)
    for count in range(img_cnt):
        img = cv2.imread(f"{count+1}.png")
        ret, img2 = cv2.threshold(img, 160, 255, cv2.THRESH_BINARY)
        # k邻域降噪
        img3 = operate_img(img2, 4)
        # 邻域非同色降噪
        img4 = noise_unsome_piexl(img3)

        cv2.imwrite(f'{count+1}.png', img4)
    os.chdir("../")   

def Recognition():

    os.chdir("./"+path_1)
    for count in range(img_cnt):
        result = pytesseract.image_to_string(f'{count+1}.png', lang="ads").replace(' ', '')[0:4]
        print(result)
    os.chdir("../")  

if __name__ == "__main__":
    GetReCapthcha()
