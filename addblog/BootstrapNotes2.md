title=Bootstrap学习笔记系列（二	）
en_title=Bootstrap
category=Web Design
tags=Bootstrap,Web
summary=前一篇文章主要介绍一下Bootstrap的引用，以及对移动设备的支持。还在最后稍微提了一下两个B的神器，container以及container-fluid，这篇文章就给大家来个详细的解说。
<ep_info>

相信很多童鞋跟小w一样，自己从0到1设计的UI都可以用怎一个字`丑的一逼`来形容，就像这样...
![](http://i.imgur.com/xjz0hQx.png)

怎一个丑字了得，在这个看脸的世界，如果做成这样估计就没有人用了。

在此提前透漏一下，这是小w目前课余做的一个所谓的智能家居的小玩意，等项目成熟之后，就会开源，大家敬请期待吧！

好了言归正传！！！

#一、栅格系统
B的栅格系统是由行和列组成的这很好理解，他把整个container进行了划分，应该不难理解，如果实在理解不了，那就去参考一下office的插入表格就好了。

栅格系统有`.row`和`.column`类组成，他们必须被包含在container中的其中之一。 同时一`.row`最多包括<font color=red>12</font>个`.column`这个是B的龟腚。当然如果包括的列多于12那么他就会自动放入下一行，建议各位太君还是老老实实不要超过12要不然会有各种诡异的UI，让你的页面看的不伦不类。

##1. 栅格参数
>![](http://i.imgur.com/Xkhacre.png)

##2. 实例
###A. Common Sense
>![](http://i.imgur.com/UZOpYwk.png)
>>![](http://i.imgur.com/LT6ikVC.png)

这其实很好理解啦，相信大家一看就明白。其实我想说的是如果每一个`class`属性设置多个值，这时候就有用了例如如果将`class`属性加上`col-xs-6`, 那么就能很好的在小尺寸的屏幕上显示了，而不用自己去规定其大小，这个自适应的过程会交给B自己实现的。

###B. 列偏移，嵌套，排序
* 使用`.col-md-offset-*`对列进行偏移。
    > ![](http://i.imgur.com/o3N0KQk.png)
 
    >> ![](http://i.imgur.com/HyktqhU.png)
* 嵌套就不展示了，跟C语言什么的嵌套是一样的，但有一点要提醒的就是，宿主作为一个container照样被分为12个column，所以嵌套之后的大小是依赖于宿主的。

* 排序通过`.col-md-push-*` 和 `.col-md-pull-*`来设置，跟偏移是一样的，但是要注意你pull或者push之后要恰好在哪个12栅格之内，要不然还是会出现换行的情况。

###C. Summary
小w感觉栅格系统是B的核心，也是能否设计出漂亮页面的关键。

1.  每个`.row`最多包括12个列；
2.  `.col-xx-xx`来定义栅格的长度；
3.  多个不同的列类可以实现对屏幕大小的自适应具体请参考栅格参数；
4.  更多精髓还在自己参悟。。。

##To continued...