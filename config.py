# -*- coding:utf-8 -*-
__author__ = 'Threedog'
__Date__ = '2018/6/4 11:16'

# 窗体标题  用于定位游戏窗体
WINDOW_TITLE = "PictureMatching3"
# 时间间隔  间隔多少秒连一次
TIME_INTERVAL = 0.01
# 游戏区域距离顶点的长度
MARGIN_LEFT = 100
# 游戏区域距离顶点的高度
MARGIN_HEIGHT = 100
# 横向的方块数量
H_NUM = 11
# 纵向的方块数量
V_NUM = 6
# 方块宽度
SQUARE_WIDTH = 65
# 方块高度
SQUARE_HEIGHT = 65

# 切片处理时候的左上、右下坐标：
# 注意  这里要么保证是21*25(因为开源代码里的empty.png提供的是21*25像素的)。如果不是（比如四个数据是10,10,50,50；也就是40*40像素），
# 那么就把empty.png图片替换成对应大小的一张图片（比如40*40）。图片可以没用，但程序中不能SUB_LT_X = 5
SUB_LT_X = 5
SUB_LT_Y = 5
SUB_RB_X = 26
SUB_RB_Y = 30

# 点击块的正中心
# SQUARE_WIDTH / 2
MOUSE_POS = 30

# 文件名常量
PIC_FOLDER = "pic"
PIC_NAME = "f{}.png"
SCREEN_PIC = "screen.png"
EMPTY_PIC = "empty.png"
