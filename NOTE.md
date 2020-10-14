## 学习笔记

> 近来无事，又研究其了之前看到过的[自动连连看的代码](https://github.com/TheThreeDog/Auto-Lianliankan)，碰到了一些问题， 因此做下笔记

**pywin32**

- win32gui：定位窗体，操作窗体
- win32api：提供API，操作鼠标、键盘
- win32con：具体API事件

## 程序的设计：

1. `getWindowPosition`=>先确定游戏窗口位置pos，并置顶
2. `getScreenImage()`==>在窗口置顶后再截图
3. `getAllSquare()`=>找到游戏边界，`pos[0]+100`, `pos[1]+100`,即中间所有图块部分。切割出所有图案；`getAllSquareTypes()`将所有图案进行比较分类，归纳出所有不同的种类

```python
# ndarray的切片方法，[纵坐标起始位置：纵坐标结束为止，横坐标起始位置：横坐标结束位置]
square = screen_image[game_y + y * SQUARE_HEIGHT :game_y + (y+1) * SQUARE_HEIGHT,
                      game_x + x * SQUARE_WIDTH:game_x + (x+1) * SQUARE_WIDTH]
# np.shape(square) == (65, 65, 3)
# 因为有些图片的边缘不一致造成干扰（主要是空白区域的切图），所以把每张小方块向内缩小一部分再
# 对所有的方块进行处理屏蔽掉外边缘 然后返回
return [square[SUB_LT_Y:SUB_RB_Y, SUB_LT_X:SUB_RB_X] for square in all_square]
```

4. `getAllSquareRecord()`==>将不同种类的图案做映射，转换成相对应的数字矩阵。
5. `autoRemove(result, board_pos)`==>执行自动消除
6. `Matcher类`==>实现游戏规则: 横消，纵消， 单拐点消除，双拐点消除。需要注意跟QQ连连看不同的是没有实现更高阶的拐点消除。

## 附录: 遇到的问题

### [列表的清空](https://www.cnblogs.com/BackingStar/p/10986775.html)

代码中有一段，在line满了后，会将line清空，再添加

```python
if len(line) == V_NUM:
    result.append(line)
    line = []
```

注意： 这边的写法`line = []`是可行的。而`line.clear()`是不行的。原因是涉及**内存空间引用问题**

原因在于: `list.clear()`会清除当前变量指向的内存地址内容，而`line = [] `其实是指向了另一块地址。因此导致了最终的结果是`line = []`的result为`[[1,2,3...], [2, 3, 4...]]`；而`list.clear()`的result全为空`[[],[],[]]]`

```python
a= [1, 2, 3]
print(id(a))
# 1785191184200
a = [1, 2]
print(id(a))
# 1785191276296
a.clear()
print(id(a))
# 1785191276296
```

### 图片的维度问题:

开源代码提供的empty.png图片规格为: 25*21像素。而25对应的为y， 21对应的为x。而需要注意的是在代码中，表达为`img[0: 25, 0: 21]`

### GetWindowRect窗口大小有误

```python
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
```

如图操作下来, 发现返回的pos为(408, 172)，但用spy++抓到的窗口左上角坐标为(510, 215)，研究发现横、纵都是1.25倍， 以为是分辨率的问题，所以打开了“显示设置”，结果正好看到了缩放布局是125%，因此问题可能出现在这个设置上，果然修改为100%后，程序能够正常运行。

额外，百度也找到了这个问题——[win32gui.GetWindowRect在win10上获取窗口宽高不正确的另一种可能](https://blog.csdn.net/snfdess/article/details/104169771?utm_medium=distribute.pc_relevant.none-task-blog-title-2&spm=1001.2101.3001.4242); [win32gui.GetWindowRect() 取值不准的解决方案](https://blog.csdn.net/See_Star/article/details/103940462)——亲测这个无效

## 附录: 

config.py中需要注意的设置

```python
# 方块宽度(算上了边界)
SQUARE_WIDTH = 65
# 方块高度(算上了边界)
SQUARE_HEIGHT = 65
# ==> 所以每块的大小为(65, 65, 3)

# 切片处理时候的左上、右下坐标：
# 注意  这里要么保证是21*25(因为开源代码里的empty.png提供的是21*25像素的)。如果不是（比如四个数据是10,10,50,50；也就是40*40像素），那么就把empty.png图片替换成对应大小的一张图片（比如40*40）。图片可以没用，但程序中不能
SUB_LT_X = 5
SUB_LT_Y = 5
# 下面两个值得小于60, 因此还有5是边界
SUB_RB_X = 26
SUB_RB_Y = 30
```