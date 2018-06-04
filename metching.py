
__author__ = 'Threedog'
__Date__ = '2018/3/12 23:57'


result = None


def canConnect(x1,y1,x2,y2,r):
    '''
    :两个方块是否可以连通函数
    '''
    # 将传入的二维数组赋值给本地全局变量，
    global result
    result = r
    # 如果有一个为0 直接返回False
    if result[x1][y1] == 0 or result[x2][y2] == 0:
        return False
    if x1 == x2 and y1 == y2 :
        return False
    if result[x1][y1] != result[x2][y2]:
        return False
    # 先判断横向可连通
    if horizontalCheck(x1,y1,x2,y2):
        return True
    # 在判断纵向可连通
    if verticalCheck(x1,y1,x2,y2):
        return True
    # 判断一个拐点的可连通情况
    if turnOnceCheck(x1,y1,x2,y2):
        return True
    # 判断两个拐点的可连通情况
    if turnTwiceCheck(x1,y1,x2,y2):
        return True
    # 都不可连通，返回false
    return False


def horizontalCheck(x1,y1,x2,y2):
    '''
    :判断水平方向能够连通
    '''

    global result
    # 判断两个不是同一个方块
    if x1 == x2 and y1 == y2:

        return False
    # 判断两个的纵坐标相同
    if x1 != x2:
        return False
    startY = min(y1, y2)
    endY = max(y1, y2)
    # 判断两个方块是否相邻
    if (endY - startY) == 1:
        return True
    # 判断两个方块通路上是否都是0，有一个不是，就说明不能联通，返回false
    for i in range(startY+1,endY):
        if result[x1][i] != 0:
            return False
    return True


def verticalCheck(x1,y1,x2,y2):
    '''
    :判断垂直方向能否连通
    '''
    global result
    # 判断不是同一个方块
    if x1 == x2 and y1 == y2:
        return False
    # 判断两个横坐标相同
    if y1 != y2:
        return False
    startX = min(x1, x2)
    endX = max(x1, x2)
    # 判断两个方块是否相邻
    if (endX - startX) == 1:
        return True
    # 判断两方块儿通路上是否可连。
    for i in range(startX+1,endX):
        if result[i][y1] != 0:
            return False
    return True


def turnOnceCheck(x1,y1,x2,y2):
    '''
    :判断单拐点情况能否连通
    '''
    global result
    # 实现单拐点校验。
    if x1 == x2 and y1 == y2:
        return False
    # 一个拐点，说明两个方块必须在不同行不同列！
    if x1 != x2 and y1 != y2:
        # cx cy dx dy 记录两个拐点的坐标
        cx = x1
        cy = y2
        dx = x2
        dy = y1
        # 拐点为空，从第一个点到拐点并且从拐点到第二个点可通，则整条路可通。
        if result[cx][cy] == 0:
            if horizontalCheck(x1, y1, cx, cy) and verticalCheck(cx, cy, x2, y2):
                return True
        if result[dx][dy] == 0:
            if verticalCheck(x1, y1, dx, dy) and horizontalCheck(dx, dy, x2, y2):
                return True
    return False


def turnTwiceCheck(x1,y1,x2,y2):
    '''
    :两个拐点的情况能否连通
    '''
    global result
    if x1 == x2 and y1 == y2:
        return False
    # 遍历整个数组找合适的拐点
    for i in range(0,len(result)):
        for j in range(0,len(result[1])):
            # 不为空不能作为拐点
            if result[i][j] != 0:
                continue
            # 不和被选方块在同一行列的
            # 不能作为拐点
            if i != x1 and i != x2 and j != y1 and j != y2:
                continue
            # 作为交点的部分也要过滤掉
            if (i == x1 and j == y2) or (i == x2 and j == y1):
                continue
            if turnOnceCheck(x1, y1, i, j) and (horizontalCheck(i, j, x2, y2) or verticalCheck(i, j, x2, y2)):
                return True
            if turnOnceCheck(i, j, x2, y2) and (horizontalCheck(x1, y1, i, j) or verticalCheck(x1, y1, i, j)):
                return True

    return False
