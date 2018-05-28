'''
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
import os

speed = 0.5
path = os.getcwd() + "\\squares\\"


# 获取窗体坐标位置(左上)
def getGameWindowPosition():
    # FindWindow(lpClassName=None, lpWindowName=None)  窗口类名 窗口标题名
    window = win32gui.FindWindow(None,"QQ游戏 - 连连看角色版")
    # 没有定位到游戏窗体
    while not window:
        print('定位游戏窗体失败，2秒后重试...')
        time.sleep(2)
        window = win32gui.FindWindow(None, "QQ游戏 - 连连看角色版")
    # 定位到游戏窗体
    win32gui.SetForegroundWindow(window) # 将窗体顶置
    pos = win32gui.GetWindowRect(window)
    print("定位到游戏窗体：" + str(pos))
    return (pos[0],pos[1])


if __name__ == '__main__':
    # time.sleep(3)
    game_pos = getGameWindowPosition()




