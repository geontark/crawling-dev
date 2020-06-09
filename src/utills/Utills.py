import time
from selenium import webdriver
import pandas as pd
import os
from PIL import Image

# chrome 브라우저 드라이버
def getChromeDriver(path):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    return webdriver.Chrome(path, options=options)

# 파일 생성하기
def createCsvFile(path):
    if os.path.isfile(path):
        print('file already exist')
    else:   # 파일 존재 하지 않으면 빈 csv 파일 생성
        data = []
        pd.DataFrame(data).to_csv(path, header=True, index=False)

# directory 생성하기
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

# target element를 window탑에 두도록한다(스크롤이동)
def movingTop(target):
    target.location_once_scrolled_into_view
    time.sleep(2)
    return target

def imgResize(imgPath, width, height):
    im = Image.open(imgPath)
    # Thumbnail 이미지 생성
    size = (width, height)
    im.thumbnail(size)
    im.save(imgPath)

def fileStrRead(filePath):
    f = open(filePath, 'r')
    result = f.read()
    f.close()
    return result