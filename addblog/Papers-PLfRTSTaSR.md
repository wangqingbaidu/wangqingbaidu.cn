title=Papers on Deep Learning(Perceptual Losses for Real-Time Style Transfer)
en_title=dlp
category=Papers
tags=DeepLearning,Papers,NeuralArt
summary=继上一篇给各位大侠介绍了码农翻身成为艺术家之后，继续给大家安利一篇新的论文，上一篇论文最大的不足就是computation costly，在GPU上弄出一个艺术照都要1-2min，这个东西想弄成实时或者对外提供服务的还真是不行，所以需要一个更好的算法可以实现快速地将照片转化成艺术照片。
<ep_info>

#[Perceptual Losses for Real-Time Style Transfer](https://arxiv.org/abs/1603.08155)
哒溜君上次给大家介绍了一个image2art的，如果你忘记了可以前去参考一下，[戳我](http://www.wangqingbaidu.cn/article/dlp1474467516.html)。

继续摆上哒溜君网红照片。

![](http://i.imgur.com/WZ0SoGx.jpg) + ![](http://i.imgur.com/SoV2ZpG.jpg) = ![](http://i.imgur.com/T9V2fdu.jpg)

##一、Method
由于[A Neural Algorithm of Artistic Style](http://arxiv.org/abs/1508.06576)论文太消耗时间，所以论文主要是针对算法的效率上进行了改进。

作者的整体思路跟前面的一样，重新生成的照片分成了2个部分，分别是`content`和`style`。`content`反映的是原始图片的信息，`style`反应的是艺术照片的信息。唯一不同点就是坐着使用一个前反馈网络完成整个图片的生成。

下面看一下整体的网络结构图。

![](http://i.imgur.com/aTpsDwj.png)

可以看到后半部分的结构图其实跟前文的结构是一样的，同样使用的是VGG16的网络作为loss获取loss的网络。

##二、Core Idea
![](http://i.imgur.com/3IzuV3v.png)

首先看看他们最主要的区别，A Neural Algorithm of Artistic Style这篇论文中，通过随机初始化一个y，然后通过若干轮的迭代，每次修改的是y的数据，以此来完成目标图像的重建。也就是说他的这个学习具有很强的灵活性，任意给定的style和content图片，都是可以进行学习的，但是这样就造成了他的一个致命的缺点，就是同一style的中间结果（或者说修改的方法没有保存，话说如果是这样训练也不知道该如何保存），造成了它的效率很低。

这篇论文的核心idea就是利用计算机领域经常使用的trick--空间换取时间，就是想一个办法可以把同样的style图片的转化方法保存一下，这样就有了前面的fW（Image Transform Net）网络，这个网络里面的参数就是保存生成指定style的变换方法。

作者的fW网络采用的是resnet。

##三、Loss Function
loss function跟前面论文的损失函数相差不大，这里就不再细说，可以参考[A Neural Algorithm of Artistic Style](http://arxiv.org/abs/1508.06576)

##四、总结
这篇论文的效率得到了极大的提升，下面看一下论文给出的数据

![](http://i.imgur.com/xpAvwDi.png)

其实这个应该来说还是挺正常的，毕竟使用的是只有一个前反馈网络。

但是他有一个最致命的缺点就是，所有的style都必须是已经提前训练好的，如果训练好的模型没有，那么就不可能实现转化，因为ys每次都是固定的，这个相比于前面的那篇论文灵活性又有不足。

下面给大家推荐一个App  [philm, 非ios好像打不开...](https://appsto.re/cn/vgtweb.i)

![](http://i.imgur.com/zgsVnd8.png)


最后哒溜君给大家透漏一个小秘密，由于工作的需要，会研究一下使用OpenGL es，实现此算法。