title=Papers on Deep Learning(R-FCN)
en_title=dlp
category=Papers
tags=DeepLearning,Papers,ObjectDetection
summary=目标检测领域，从rbg大神提出之后，到目前逐渐分化出2大阵营，一种是以Proposal+classification为主的multi-stage的方法，另一种是以YOLO为代表的End2End的模型，前一种模型特点就是精度高，后一种的特点是速度快，但是后面肯定end2end也会达到multi-stage的精度。
<ep_info>

[转帖请注明出处www.wangqingbaidu.cn](www.wangqingbaidu.cn)
#[R-FCN: Object Detection via Region-based Fully Convolutional Networks](https://arxiv.org/abs/1605.06409)

目标检测任务目前分成两种解决方法，一个是以R-CNN为代表的多阶段的任务（multi-stage pipeline）另一个是最近的以YOLO为代表的end-to-end的处理方式。End2end的方法在解决这个任务的过程中，将目标分类，bbox的回归全部融合到了一个完整的网络，最后通过全连接实现最终的任务。由于end-2-end的方法只有一个阶段，所以在运行效率上是其优势。通过proposal的方法一般是两个阶段，但是随着Faster R-CNN方法的提出，这两个阶段开始共享一些卷积的运算，由此在效率上也有所提升。
R-FCN主体使用的是Faster R-CNN的idea，但是由于后者虽然与RPN会共享一定的卷积结果，但是后面的分类以及回归网络都是单独的，所以在性能上还是有可以提升的地方。

##一、Introduction
看一下目标检测任务，首先他回答的是两个问题，分别是，`是什么？`以及`在那？`两个问题，`是什么`是位置无关的，也就是一副狗的图片无论你是狗是在左上角还是右上角都是无所谓的，但是`在那`这个问题就是位置有关了，就是如果检测的目标是一只狗，但是本来它在左上角，如果框定的bbox在有下角显然就是错误了。

![](http://i.imgur.com/Tkei3QS.jpg)

所以目标检测就分成两大派系，Multi-stage以及End to End，多阶段的策略在YOLO之前是比较流行的，从R-CNN到这篇文章，但是今年YOLO以及SSD的工作进行端到端的训练，在速度上得到了很大的提升，同时精度也是越来越高。

##二、Related Work
接下来简单回顾一下相关的工作，R-CNN通过Selective Search提取Proposal，然后进行Proposal wise地进行预测，效率还是奇低的，但是由于是目标检测开创性的工作，所以还是有奠基作用的，后面的就是Spp Net，同样是Selective Search提取，但是由于不同的Proposal共享在一张图片上，所以他共享了卷积运算的结果，在之后就是Faster R-CNN，他最大的地方就是把Proposal的提取融合到了网络中，最大限度的共享了卷积网络的结果，但是还是有一定的冗余计算。相面这个图给出了各个极端共享网络参数的情况（作者实现的是ResNet-101）

![](http://i.imgur.com/x3XvODI.png)

R-FCN的出发点就是，能不找到一种方法可以最大限度的使用共享网络参数，也就是上层的，在PRN网络之后我是不是可以直接得到分类的结果。

##三、Architecture
![](http://i.imgur.com/q6j67M3.png)

从图片到RPN的网络就不再过多的赘述，只是简单的说一下，如果不明白可以参考其他的Faster R-CNN的blog 或者论文。

>conv -> feature map, 作者使用的ResNet-101, 进行图片的特征提取。
>
>conv -> RPN, 与Faster R-CNN类似，进行Proposal的提取。

详细介绍下面的这个网络结构

![](http://i.imgur.com/IYWJNIY.png)

在卷积的最后一层，通过k×k×(c+1)个卷积核，生成对应个数的feature map，其中C是数据的类别的个数。K是预定义的超参，论文实现中，作者使用的是3，下面也已k=3举例。

对于每一个类别，一共是有9（3×3）个feature map, 这是分别编号1-9，对应于下图的从上到下，从左到右。

![](http://i.imgur.com/dzdck9K.png)

每一个RoI对应一块的feature map 中的区域，根据前面的k=3，可以将这块区域平均分成9份，标记为上左，上中，上右……在形成后面的score map 的时候，分别取编号1的feature map的上左，编号2的feature map 的上中……分别进行pooling，文中使用的是avgpooling，然后形成3×3=9的score  map，然后对这9个数，进行投票，作者使用average为投票分值，来判断这个RoI的位置是不是恰到好处。

这个pooling的具体细节使用下面的公式

$$r_c(i,j|\theta)=\sum_{(x,y)\in bin(i,j)}\frac{z_{i,j,c}(x+x_0, y+y_0|\theta)}{n}$$

>rc：每一个分类的分数, C+1类；
>
>z为对应分类的得分；
>
>x0，y0为Proposal的对应位置；
>
>n为Proposal的像素点个数。

##四、Experiments
VOC2007的测试结果

>![](http://i.imgur.com/BTVXRnz.png)

VOC2012的测试结果
>![](http://i.imgur.com/jNNZUwn.png)

##五、Summary
这篇文章和SSD，YOLO等在利用feature map的时候有异曲同工之妙，都是讲前面的feature map 赋予了不同的任务含义，YOLO只是使用了最后一层的feature map，而SSD则是使用了最后的若干层进行特定任务，R-FCN同理。

不同于前面的Conv层仅限于提取特征，这三种方法都更细粒度的使用了前面网络提取的feature map，这个哒溜君感觉在其他的一些任务上应该或多或少得有借鉴意义。