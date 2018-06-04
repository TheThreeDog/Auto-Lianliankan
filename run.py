'''
python 版本：3.5
opencv 下载链接： 
https://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv
选择版本：opencv_python‑3.4.1‑cp35‑cp35m‑win_amd64.whl
pywin32 下载链接：
https://www.lfd.uci.edu/~gohlke/pythonlibs/#pywin32
选择版本：pywin32-223-cp35-cp35m-win_amd64.whl 
'''

import metching
import cv2
import numpy as np
import win32api
import win32gui
import win32con
from PIL import ImageGrab
import time
from config import *


# 获取窗体坐标位置(左上)
def getGameWindowPosition():
    # FindWindow(lpClassName=None, lpWindowName=None)  窗口类名 窗口标题名
    window = win32gui.FindWindow(None,WINDOW_TITLE)
    # 没有定位到游戏窗体
    while not window:
        print('定位游戏窗体失败，5秒后重试...')
        time.sleep(5)
        window = win32gui.FindWindow(None,WINDOW_TITLE)
    # 定位到游戏窗体
    win32gui.SetForegroundWindow(window) # 将窗体顶置
    pos = win32gui.GetWindowRect(window)
    print("定位到游戏窗体：" + str(pos))
    return (pos[0],pos[1])

# 获取一张完整的屏幕截图
def getScreenImage():
    print('捕获屏幕截图...')
    scim = ImageGrab.grab()  # 屏幕截图，获取到的是Image类型对象
    scim.save('screen.png')
    return cv2.imread("screen.png") # opencv 读取，拿到的是ndarray存储的图像


if __name__ == '__main__':
    # 1、定位游戏窗体
    game_pos = getGameWindowPosition()
    time.sleep(1)
    # 2、从屏幕截图一张，通过opencv读取
    screen_image = getScreenImage()

    cv2.waitKey(0)
    cv2.destroyAllWindows()







