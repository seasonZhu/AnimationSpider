# AnimationSpider

浓浓Swift风格的Python编码.

其实是我懒得每天跑去下载种子,于是乎想着怎么个懒法.

本代码仅供学习使用,如果下载中出现什么问题,请注意修改Constant.py文件中的seedFilePath路径.

本代码仅在MacOS上运行良好,没有在Windows平台进行测试.

本代码依赖第三方库requests和BeautifulSoup和lxml,部分使用lxml框架进行解析,只是为了学习使用Xpath方式进行爬虫.

本代码由python3编写.

如果有什么什么问题,欢迎pullRequest,另外,请不要过于频繁的爬虫.

2021年5月14日

今天修复了崩溃的一些bug,说实话Python的安全需要细致判断来进行.

我考虑更多的使用try来进行优化.

目前我对于爬虫的获取的信息的边界进行了优化,但是还是避免不了由于网页异常导致的问题.

另外,把一些其他的爬虫例子做了整理.

运行本程序,在Main.py下面run就可以了.
