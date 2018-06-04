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

# 从屏幕截图中识别
def getAllSquare(screen_image,game_pos):
    print('图像切片处理...')
    # 通过游戏窗体，找到连连看连接的区域：
    game_x = game_pos[0] + MARGIN_LEFT
    game_y = game_pos[1] + MARGIN_HEIGHT
    # 从连接区域左上开始，把图像切割成一个一个的小块，切割标准是按照小块的横纵坐标。
    all_square = []
    for x in range(0,H_NUM):
        # line_square = []
        for y in range(0,V_NUM):
            # ndarray的切片方法，[纵坐标起始位置：纵坐标结束为止，横坐标起始位置：横坐标结束位置]
            square = screen_image[game_y + y * SQUARE_HEIGHT :game_y + (y+1) * SQUARE_HEIGHT,game_x + x * SQUARE_WIDTH:game_x + (x+1) * SQUARE_WIDTH]
            all_square.append(square)
    # 因为有些图片的边缘不一致造成干扰（主要是空白区域的切图），所以把每张小方块向内缩小一部分再
    # 对所有的方块进行处理屏蔽掉外边缘 然后返回
    return list(map(lambda square : square[SUB_LT_Y:SUB_RB_Y,SUB_LT_X:SUB_RB_X],all_square))
    # 上面这行相当于下面这4行
    # new_all_square = []
    # for square in all_square:
    #     s = square[SUB_LT_Y:SUB_RB_Y, SUB_LT_X:SUB_RB_X]
    #     new_all_square.append(s)
    # return new_all_square


if __name__ == '__main__':
    # 1、定位游戏窗体
    game_pos = getGameWindowPosition()
    time.sleep(1)
    # 2、从屏幕截图一张，通过opencv读取
    screen_image = getScreenImage()
    # 3、图像切片，把截图中的连连看切成一个一个的小方块，保存在一个数组中
    all_square_list = getAllSquare(screen_image,game_pos)

    cv2.waitKey(0)
    cv2.destroyAllWindows()







