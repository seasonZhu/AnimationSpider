from pyquery import PyQuery as pq

# 简单的访问
s = '<html><title>PyQuery用法总结<title></html>'
doc = pq(s)
print(doc('title'))
print(doc.text())
print(doc.html())

# 直接访问网页
url = 'https://www.hao123.com'
doc = pq(url=url,encoding='utf-8')
print(doc('title').text())

# 访问属性
li = pq('<li id="test1" class="test1"></li><li id="test2" class="test2"></li>')('li')
print(li.attr("id"))

# 上面的代码中有两个id不同的li节点，但是attr()方法只取第一个li节点的id属性值，
# 而不取第二个，我们把上面的代码修改下，把第一个li节点的id属性去掉，attr方法是否只取第一个复合条件节点的属性值：
li = pq('<li class="test1"></li><li id="test2" class="test2"></li>')('li')
print(li.attr("id"))

# 第一个li节点没有id属性，因此返回结果为None，所以可见，attr()方法返回的是第一个节点的属性值。
#那要取多个li节点的属性值，要怎么做呢？这就要结合items()方法来实现。items()方法是返回的节点的生成器generator object PyQuery.items
li = pq('<li id="test1" class="test1"></li><li id="test2" class="test2"></li>')('li')
print(li.items())
for item in li.items():
    print(item.attr("id"))

# 动态添加节点class属性
html = '<li id="test1" class="test1"></li>'
li = pq(html)('li')
li.addClass("addClass")
print(li)

# 动态添加其他属性
html = '<li id="test1" class="test1"></li>'
li = pq(html)('li')
li.attr("name","li name")
print(li)
li.attr("type","li")
print(li)
print(li.attr("type"))

# 动态添加/修改文本值
html = '<li id="test1" class="test1"></li>'
li = pq(html)('li')
li.html("use html() dynamic add text")
print(li)
li.text("use text() dynamic add text")
print(li)

# 获取节点文本值
html = '<li id = "test_id">li text value</li>'
li = pq(html)('li')
print(li.text())
print(li.html())

# remove()方法可以动态移除节点：
html = '''
<ul>
hello I am ul tag
<li>hello I am li tag</li>
</ul>
'''
ul = pq(html)('ul')
print(ul.text())
print('执行remove()移除节点')
ul.find('li').remove()
print(ul.text())

# 支持使用css的.和#来查找节点：
html = '''
<div class="div_tag">
<ul id = "ul_tag">
hello I am ul tag
<li>hello I am li tag</li>
<li>hello I am li tag too</li>
</ul>
</div>
'''
doc = pq(html)
print(doc('.div_tag #ul_tag li'))
# 也可以通过find进行查找
print(doc('.div_tag #ul_tag').find("li"))
# children 是获取当前节点的所有子节点
print(doc.children('#ul_tag').find("li"))

# siblings()方法返回当前节点的兄弟节点：
html = '''
<div class="div_tag">
<ul id = "ul_tag">
hello I am ul tag
<li class="li_class1">hello I am li tag<a>www.bigdata17.com</li>
<li class="li_class2">hello I am li tag too</li>
<li class="li_class3">hello I am the third li tag</li>
</ul>
</div>
'''
doc = pq(html)
print(doc('.div_tag #ul_tag .li_class1').siblings())

# sibligs()还支持传入css选择器筛选符合条件的li节点：
print(doc('.div_tag #ul_tag .li_class1').siblings('.li_class3'))