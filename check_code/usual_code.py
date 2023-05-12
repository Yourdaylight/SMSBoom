# -*- coding: utf-8 -*-
# @Time    :2023/5/4 8:02
# @File    : usual_code.py
# @Software: PyCharm
# 普通四字母验证码

import time
import cv2 as cv
import pytesseract
from PIL import Image
import requests
import numpy as np


def recognize_text(image_url):
    # 使用OpenCV解码图像
    image = cv.imread(image_url)
    blur = cv.pyrMeanShiftFiltering(image, sp=8, sr=60)
    # 灰度图像
    gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
    # 二值化
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
    print(f'二值化自适应阈值：{ret}')
    # 形态学操作  获取结构元素  开操作
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 2))
    bin1 = cv.morphologyEx(binary, cv.MORPH_OPEN, kernel)
    kernel = cv.getStructuringElement(cv.MORPH_OPEN, (2, 3))
    bin2 = cv.morphologyEx(bin1, cv.MORPH_OPEN, kernel)
    # 逻辑运算  让背景为白色  字体为黑  便于识别
    cv.bitwise_not(bin2, bin2)
    # 识别
    test_message = Image.fromarray(bin2)
    text = pytesseract.image_to_string(test_message)
    print(f'识别结果：{text}')


def save_image(image_url,name="code.jpg"):
    # 图片保存到本地
    response = requests.get(image_url)
    with open(name, 'wb') as f:
        f.write(response.content)

available = {
    # 中昱维信
    "https://vip.veesing.com/vip-web/register/vcode": {
        # 验证码地址
        "code": "https://vip.veesing.com/vip-web/register/photocode?timestamp=%s",
        # 发送验证码参数
        "parameter": {
            "phone": "18600000000",
            "code": "1234"
        },
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "referer": "https://vip.veesing.com/",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; Redmi K30 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Mobile Safari/537.36"
        }
    },
    # 逐浪小说
    "https://www.zhulang.com/home/login/sendCode.html": {
        "code": "https://www.zhulang.com/login/verify.html?_t=%s",
        "parameter": {
            "phone": "18600000000",
            "code": "1234"
        },
        # 验证码参数映射,如果验证码参数名不是code,则需要映射
        "map_param": {
            "code": "charcode"
        },
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "referer": "https://www.zhulang.com/login/phone.html",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; Redmi K30 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Mobile Safari/537.36"
        }
    }
}

for index,target in enumerate(available):
    img_name = "code_%s.jpg" % str(index)
    save_image(available[target]["code"] % str(time.time() * 1000),img_name)
    validate_code = recognize_text(img_name)
    if "map_param" in available[target]:
        for key in available[target]["map_param"]:
            available[target]["parameter"][available[target]["map_param"][key]] = validate_code
            # delte the old key
            del available[target]["parameter"][key]
    else:
        available[target]["parameter"]["code"] = validate_code
    available[target]["parameter"]["phone"] = "13886686058"
    # post提供表单数据
    response = requests.post(target, data=available[target]["parameter"], headers=available[target]["headers"])
    try:
        print(response.json())
    except:
        print(response.text)

# for url in ["code.jpg","code_0.jpg","code_1.jpg"]:
#     recognize_text(url)
