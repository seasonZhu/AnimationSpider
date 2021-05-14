# 今天看了一篇Python的文章,才发现还有这种写法,这基本上和Swift没什么区别了
def swiftStyle():
    """ 一个Swift风格的函数表达式 """
    a: str = "aa"
    b: int = 1

    # 参数和返回标注了类型，那么接下来调用时就能进行提示
    def example(a: str) -> str:
        return f"Hello {a}"

    print(example(a = "world"))

    # 一些简单的标注，看起来起不到效果，但如果换个有含义的名字呢
    User = str
    Age = int
    Answer = str

    def say_hello(u: User) -> Answer:
        """ 输入用户信息,返回回答 """
        return f"Hello {u}"

    print(say_hello("Shadow"))

if __name__ == "__main__":
    swiftStyle()