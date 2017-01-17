title=markdown入门
en_title=markdown_introduction
category=markdown
tags=DEdit,Markdown
summary=此博客网站中的所有博客都是使用markdown语法进行编辑的，接下来给大家安利一发markdown。
<ep_info>
#####写这篇博客很兴奋，因为它包括了我诸多的第一次；第一篇自己的博文(不算cnblog)，第一次使用markdown，这个博客网站的第一篇正式博客，这也是我在个人博客里面的FB...

不扯废话了，还是赶快给大家介绍markdown，这个神奇的文本编辑的语法。我尽量涵盖所有的内容，当然不可能是全部，如果有不全的还请大家指出。

首先说为什么使用markdown，你可能会问我有word啊，那个东西不是功能很完善吗？这个问题很好，word功能太强大了，简直无所不包啊，但就是因为他太强大了，我们常用的word功能又有几个能，我想无非就是设置一下首行缩进，弄一下字体颜色罢了。但是有句古话说的非常好，浓缩的都是精品，markdown就是那个精品。

#[Markdown设计初衷](http://www.appinn.com/markdown/)

Markdown 的目标是实现「易读易写」。

可读性，无论如何，都是最重要的。一份使用 Markdown 格式撰写的文件应该可以直接以纯文本发布，并且看起来不会像是由许多标签或是格式指令所构成。Markdown 语法受到一些既有 text-to-HTML 格式的影响，包括 Setext、atx、Textile、reStructuredText、Grutatext 和 EtText，而最大灵感来源其实是纯文本电子邮件的格式。

总之， Markdown 的语法全由一些符号所组成，这些符号经过精挑细选，其作用一目了然。比如：在文字两旁加上星号，看起来就像*强调*。Markdown 的列表看起来，嗯，就是列表。Markdown 的区块引用看起来就真的像是引用一段文字，就像你曾在电子邮件中见过的那样。

##1.标题
标题可以使用若干个#来指定，#越多字体越小，当然也可以使用=========（高阶标题），--------（第二阶标题）
例子
### #这是 H3

##### ##这是 H5# 

###### ######这是 H6
如果为了美观可以在后面加上一定数量的#，但这是你会疑惑了，要是我标题末尾有#怎么办,那就在行末加个空格就行了。

##2.区块引用 Blockquotes
另一个很重要的东西就是看起来区块，效果就是这样的
>仅仅就是一个演示效果
>    >再来一发

使用区块，只需要在区块前面加上>就可以了，可以使用多个>进行嵌套使用，区块是以空白行(不可见字符组成)作为结束标志的。同一个区块可以略去（小w不推荐）第一个之后的>
当然引用的区块内也可以使用其他的 Markdown 语法，包括标题、列表、代码区块等：
下面的形式都是允许的
>     > ## 这是一个标题。
>     > 1.   这是第一行列表项。
>     > 2.   这是第二行列表项。

##3.列表
无序列表使用星号、加号或是减号作为列表标记：有序列表使用数字加上.(会自动忽略数字顺序，但是小w建议还是按照套路来，万一哪天markdown兴起已更新，支持有序列表的 start 属性，那就等着DYM吧!)
列表和区块是一样的一空白行作为结束，无序列表可以不进行缩进，但是有序列表必须进行缩进，要不让就相当于不再同一列表，那就从头开始把

1.  This is a list item with two paragraphs. Lorem ipsum dolor
    sit amet, consectetuer adipiscing elit. Aliquam hendrerit
    mi posuere lectus.

    Vestibulum enim wisi, viverra nec, fringilla in, laoreet
    vitae, risus. Donec sit amet nisl. Aliquam semper ipsum
    sit amet velit.

2.  Suspendisse id sem consectetuer libero luctus adipiscing.

怎么样是不是很炫。

##4.代码区块
作为码农，这是我们最关心的，没有代码区块，看着一坨字母的代码，就想看看一坨坨的蛆。但是有了代码区块，可以让自己很方便的定位到代码位置。简简单单缩进一个tab(或者4个字符就行)

	def IM_CODE_BLOCK:	
		return 'I love wangqingbaidu!'

如果你要在一段文字中插入代码怎么办，markdown早就为你想好了。在任何位置插入两个反引号`` `some code` ``，里面的就自动会成为代码了

##5.连接
连接也是经常会用到的一个属性，比如可以帮助我们迅速找到引用的地方，比如说小w最近一直在纠结于[Pixel RNN](http://159.226.251.229/videoplayer/1601.06759v2.pdf?ich_u_r_i=b0d8846e0249c8afc36388aae7086f0b&ich_s_t_a_r_t=0&ich_e_n_d=0&ich_k_e_y=1645048911751363292449&ich_t_y_p_e=1&ich_d_i_s_k_i_d=9&ich_u_n_i_t=1)的实现（google deepmin写的论文就是吊炸天，模型不给，代码不给，各种让你瞎猜。。。），使用引用就可以帮助你迅速找到PRNN是什么鬼, 看到这里，相信上面的连接你已经点开了，哈哈，又跟你开玩笑了。

连接的方式很多，下面就简单总结几种

1.使用`[example](url "title")`就可以建立指向性的连接了。

2.你如果不值现在连接的地址，也可以添加连接的id，`[example] [id]`进行指定，你可以在文章的任何地方使用`[id]: url "title"`进行定向。

3.当然前面这两种方法都太TM eggache了，能不能有点给人用的方法，哎，markdown还真有， `[word]` 在文章任何地方加上`[word]: link`就可以了。

##6.强调
Markdown 使用星号（\*）和底线（\_）作为标记强调字词的符号，被 \* 或 \_ 包围的字词会被转成用 `<em>` 标签包围，用两个 \* 或 \_ 包起来的话，则会被转成 `<strong>`

##7.反斜杠
markdown中具有特殊含义的标示符，如果在文档中要显示使用，那就要使用反斜杠` \ ` 以免让markdown解释器误解。

##8.图片链接
可以插入图片也是markdown的一个比较好的特性，使用起来也很简单`![Alt text](/path/to/img.jpg)`

详细叙述如下：

* 一个惊叹号 !
* 接着一个方括号，里面放上图片的替代文字
* 接着一个普通括号，里面放上图片的网址，最后还可以用引号包住并加上 选择性的 'title' 文字。

具体的效果是这样的

![cang](http://i.imgur.com/cV05OO5.jpg "苍老师")

其中图片有一个很好的作用是显示LaTeX公式，其原理就是将LaTeX公式公国LaTeXurl转化成一个图片。

`![](http://latex.codecogs.com/gif.latex?\prod(n_{i})+1)` 

![](http://latex.codecogs.com/gif.latex?\prod(n_{i})+1)

##9.小技巧
1.如何在反引号代码快中插入反引号？
	
>``` `` `something` ``    ```，使用两个反引号，用空格隔开。

2.未完待续



