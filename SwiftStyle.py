import math

""" 今天看了一篇Python的文章,才发现还有这种写法,这基本上和Swift没什么区别了 """
def swiftStyle():
    """ 一个Swift风格的函数表达式 """
    a: str = "aa"
    b: int = 1

    # 虽然a被定义成了str类型,但是这里还是可以对a赋值2,并且不会报错,print也没什么异常
    a = 2
    print(a)

    isinstance(a, int)

    # 参数和返回标注了类型，那么接下来调用时就能进行提示
    def example(a: str) -> str:
        return f"Hello {a}"

    print(example(a = "world"))

    # 一些简单的标注，看起来起不到效果，但如果换个有含义的名字呢
    User = str
    Age = int
    Answer = str

    Location = (float, float)

    Distance = float

    def distanceBetweenPoint1(point, toPoint):
        x1, y1 = toPoint
        x2, y2 = point
        dx = x1 - x2
        dy = y1 - y2
        distance = math.sqrt(dx * dx + dy * dy) # (dx * dx + dy * dy) ** 0.5
        return distance

    def distanceBetweenPoint2(point: Location, toPoint: Location):
        x1, y1 = toPoint
        x2, y2 = point
        dx = x1 - x2
        dy = y1 - y2
        distance = math.sqrt(dx * dx + dy * dy)
        return distance

    def distanceBetweenPoint3(point: Location, toPoint: Location) -> Distance:
        x1, y1 = toPoint
        x2, y2 = point
        dx = x1 - x2
        dy = y1 - y2
        distance = math.sqrt(dx * dx + dy * dy)
        return distance

    def say_hello(u: User) -> Answer:
        """ 输入用户信息,返回回答 """
        return f"Hello {u}"

    print(say_hello("Shadow"))

    distance1 = distanceBetweenPoint1((0, 2), (5, 7))
    print(distance1)

    distance2 = distanceBetweenPoint2(point=(0, 2), toPoint=(5, 7))
    print(distance2)

    distance3 = distanceBetweenPoint3(point=(0, 2), toPoint=(5, 7))
    print(distance3)

    # 这么写会崩溃
    #distance4 = distanceBetweenPoint3(point="haha", toPoint="hehe")
    #print(distance4)

if __name__ == "__main__":
    swiftStyle()