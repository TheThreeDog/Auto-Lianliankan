'''
python 版本：3.5
opencv 下载链接： 
https://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv
选择版本：opencv_python‑3.4.1‑cp35‑cp35m‑win_amd64.whl
pywin32 下载链接：
https://www.lfd.uci.edu/~gohlke/pythonlibs/#pywin32
选择版本：pywin32-223-cp35-cp35m-win_amd64.whl 
'''

from matcher import Matcher
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
    # 定位到游戏窗体, 将窗体顶置
    win32gui.SetForegroundWindow(window)
    pos = win32gui.GetWindowRect(window)
    print("定位到游戏窗体：" + str(pos))
    return (pos[0], pos[1])


# 获得游戏棋盘的坐标
def getGameBoard(game_pos: (int, int)):
    return game_pos[0] + MARGIN_LEFT, game_pos[1] + MARGIN_HEIGHT


# 获取一张完整的屏幕截图
def getScreenImage():
    print('捕获屏幕截图...')
    scim = ImageGrab.grab()  # 屏幕截图，获取到的是Image类型对象
    scim.save(SCREEN_PIC)
    return cv2.imread(SCREEN_PIC)  # opencv 读取，拿到的是ndarray存储的图像


# 从屏幕截图中识别
def getAllSquare(screen_image, board_pos):
    print('图像切片处理...')
    # 通过游戏窗体，找到连连看连接的区域：
    game_x, game_y = board_pos
    # 从连接区域左上开始，把图像切割成一个一个的小块，切割标准是按照小块的横纵坐标。
    all_square = []
    for x in range(0, H_NUM):
        # line_square = []
        for y in range(0, V_NUM):
            # ndarray的切片方法，[纵坐标起始位置：纵坐标结束为止，横坐标起始位置：横坐标结束位置]
            square = screen_image[
                         game_y + y * SQUARE_HEIGHT: game_y + (y+1) * SQUARE_HEIGHT,
                         game_x + x * SQUARE_WIDTH: game_x + (x+1) * SQUARE_WIDTH
                     ]
            all_square.append(square)
    # 因为有些图片的边缘不一致造成干扰（主要是空白区域的切图），所以把每张小方块向内缩小一部分再
    # 对所有的方块进行处理屏蔽掉外边缘 然后返回
    return [square[SUB_LT_Y:SUB_RB_Y, SUB_LT_X:SUB_RB_X] for square in all_square]


# 判断图像是否与已经在列表中的图像相同，如果是返回True
def isImageExist(img,img_list):
    for existed_img in img_list:
        b = np.subtract(existed_img, img)  # 图片数组进行比较，返回的是两个图片像素点差值的数组，
        if not np.any(b):   # 如果全部是0，说明两图片完全相同。
            return True
        else:
            continue
    return False

# 获取所有的方块类型
def getAllSquareTypes(all_square):
    print("将图像矩阵按类型归入类型列表...")
    types = []
    # 先把空白添加到数组中，作为0号
    empty_img = cv2.imread(EMPTY_PIC)
    types.append(empty_img)
    for square in all_square:
        # 如果这个图像不存在的话将图像保存起来
        if not isImageExist(square, types):
            types.append(square)
    return types


# 将所有的方块与类型进行比较，转置成数字
def getAllSquareRecord(all_square_list, types):
    print("将所有的方块与类型进行比较，转置成数字矩阵...")
    record = []  # 整个记录的二维数组
    line = []   # 记录一行
    for square in all_square_list:   # 把所有的方块和保存起来的所有类型做对比
        for n, tp in enumerate(types):
            res = cv2.subtract(square, tp)
            if not np.any(res):         # 如果是一样的
                line.append(n)
                break

        if len(line) == V_NUM:         # 如果校验完这一行已经有了11个数据，则另起一行
            record.append(line)
            line = []
    # print(record)
    return record


# 鼠标点击
def MouseClickDownUp(x:int, y:int):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


# 自动消除
def autoRelease(result, board_pos):
    game_x, game_y = board_pos
    for i in range(0,len(result)):
        for j in range(0,len(result[0])):
            # 以上两个for循环，定位第一个选中点
            if result[i][j] != 0:
                for m in range(0, len(result)):
                    # for n in range(j, len(result[0])):
                    # 优化地方——从左上往右下遍历不回头-->放开到右侧
                    for n in range(0, len(result[0])):
                        if result[m][n] != 0:
                            # 后两个for循环定位第二个选中点
                            if Matcher.canConnect(i, j, m, n, result):
                                # 执行消除算法并返回
                                result[i][j] = 0
                                result[m][n] = 0
                                print('可消除点：'+ str(i+1) + ',' + str(j+1) + '和' + str(m+1) + ',' + str(n+1))
                                x1 = game_x + j*SQUARE_WIDTH
                                y1 = game_y + i*SQUARE_HEIGHT
                                x2 = game_x + n*SQUARE_WIDTH
                                y2 = game_y + m*SQUARE_HEIGHT

                                # 鼠标操作1
                                MouseClickDownUp(x1 + MOUSE_POS, y1 + MOUSE_POS)
                                time.sleep(TIME_INTERVAL)
                                # 鼠标操作2
                                MouseClickDownUp(x2 + MOUSE_POS, y2 + MOUSE_POS)
                                time.sleep(TIME_INTERVAL)
                                return True
    return False


def autoRemove(squares, board_pos):
    # 判断是否消除完了？如果没有的话，点击重列后继续消除
    while np.any(squares):
        autoRelease(squares, board_pos)
        print(squares)
    print("Done!")


def saveAllTypes(types):
    """
    因为切割出来的图片发现有不一样的, 因此保存下来看区别
    :param types:
    :return:
    """
    import os
    from PIL import Image
    if not os.path.exists(PIC_FOLDER):
        os.mkdir(PIC_FOLDER)
    for i, ty in enumerate(types):
        im = Image.fromarray(ty)
        file_name = PIC_NAME.format(i)
        im.save(os.path.join(DIRECT, file_name))


if __name__ == '__main__':
    # 1、定位游戏窗体
    game_pos = getGameWindowPosition()
    # 2、从屏幕截图一张，通过opencv读取
    screen_image = getScreenImage()
    board_pos = getGameBoard(game_pos)
    # 3、图像切片，把截图中的连连看切成一个一个的小方块，保存在一个数组中
    all_square_list = getAllSquare(screen_image, board_pos)
    # 4、切片处理后的图片，相同的作为一种类型，放在数组中。
    types = getAllSquareTypes(all_square_list)
    # 原代码中发现有时无法全部消除, 因此写的一个查错函数
    # saveAllTypes(types)
    # 5、将切片处理后的图片，转换成相对应的数字矩阵。注意 拿到的数组是横纵逆向的，转置一下。
    result = np.transpose(getAllSquareRecord(all_square_list, types))
    # 6、执行自动消除
    autoRemove(result, board_pos)
    # 7、消除完成，释放资源。
    cv2.waitKey(0)
    cv2.destroyAllWindows()







