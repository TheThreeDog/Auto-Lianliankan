
__author__ = 'Threedog'
__Date__ = '2018/3/12 23:57'


class Matcher:
    result = []

    @classmethod
    def canConnect(cls, x1, y1, x2, y2, r):
        """
        两个方块是否可以连通函数
        :param x1: 第几行
        :param y1: 第几列
        :param x2: 第几行
        :param y2: 第几列
        :param r:  目前棋盘
        :return:
        """
        # 将传入的二维数组赋值给本地全局变量，
        cls.result = r
        # 如果有一个为0 直接返回False
        if cls.result[x1][y1] == 0 or cls.result[x2][y2] == 0:
            return False
        if x1 == x2 and y1 == y2:
            return False
        if cls.result[x1][y1] != cls.result[x2][y2]:
            return False
        # 先判断横向可连通
        if cls.horizontalCheck(x1, y1, x2, y2):
            return True
        # 在判断纵向可连通
        if cls.verticalCheck(x1, y1, x2, y2):
            return True
        # 判断一个拐点的可连通情况
        if cls.turnOnceCheck(x1, y1, x2, y2):
            return True
        # 判断两个拐点的可连通情况
        if cls.turnTwiceCheck(x1, y1, x2, y2):
            return True
        # 都不可连通，返回false
        return False

    @classmethod
    def horizontalCheck(cls, x1, y1, x2, y2):
        '''
        :判断水平方向能够连通
        '''

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
        for i in range(startY + 1, endY):
            if cls.result[x1][i] != 0:
                return False
        return True

    @classmethod
    def verticalCheck(cls, x1, y1, x2, y2):
        '''
        :判断垂直方向能否连通
        '''
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
        for i in range(startX + 1, endX):
            if cls.result[i][y1] != 0:
                return False
        return True

    @classmethod
    def turnOnceCheck(cls, x1, y1, x2, y2):
        '''
        :判断单拐点情况能否连通
        '''
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
            if cls.result[cx][cy] == 0:
                if cls.horizontalCheck(x1, y1, cx, cy) and cls.verticalCheck(cx, cy, x2, y2):
                    return True
            if cls.result[dx][dy] == 0:
                if cls.verticalCheck(x1, y1, dx, dy) and cls.horizontalCheck(dx, dy, x2, y2):
                    return True
        return False

    @classmethod
    def turnTwiceCheck(cls, x1, y1, x2, y2):
        """
        两个拐点的情况能否连通
        """
        if x1 == x2 and y1 == y2:
            return False
        # 遍历整个数组找合适的拐点
        for i in range(0, len(cls.result)):
            # for j in range(y1, len(cls.result[1])):
            # 优化地方——从左上往右下遍历不回头 -->放开到右侧
            for j in range(0, len(cls.result[1])):
                # 1. 过滤3种情况
                # 1.1. 不为空不能作为拐点
                if cls.result[i][j] != 0:
                    continue
                # 1.2. 不和被选方块在同一行列的, 不能作为拐点
                if i != x1 and i != x2 and j != y1 and j != y2:
                    continue
                # 1.3. 作为交点的部分也要过滤掉
                if (i == x1 and j == y2) or (i == x2 and j == y1):
                    continue
                # 优化结果:
                # 找到的拐点可能是→↓、→↑，也可能是↓→、↑→
                # 分别对应→(不存在←的情况)， ↓(不存在↑的情况)
                # 由于只放开了右侧， 所以完全不需要考虑拐点在左侧的情况，所以不需要原代码中第2个if
                if cls.turnOnceCheck(x1, y1, i, j) and \
                        (cls.horizontalCheck(i, j, x2, y2) or cls.verticalCheck(i, j, x2, y2)):
                    return True
                # if cls.turnOnceCheck(i, j, x2, y2) and \
                #         (cls.horizontalCheck(x1, y1, i, j) or cls.verticalCheck(x1, y1, i, j)):
                #     return True

        return False
