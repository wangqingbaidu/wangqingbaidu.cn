title=Papers on Deep Learning(FCN for Semantic Segmentation)
en_title=dlp
category=Papers
tags=DeepLearning,Papers,Segmentation,FCN
summary=CNN对图像的分类任务已经非常精准（实验室数据下），但是怎么样才能识别图片中特定部分的物体，在2015年之前还是一个很有挑战性的任务，这篇论文就给它指明了一个方向。
<ep_info>

[转帖请注明出处www.wangqingbaidu.cn](www.wangqingbaidu.cn)

部分素材参考[http://www.cnblogs.com/gujianhan/p/6030639.html](http://www.cnblogs.com/gujianhan/p/6030639.html)
#[Fully Convolutional Networks for Semantic Segmentation](https://arxiv.org/abs/1411.4038)
与经典的CNN在卷积层之后使用全连接层（限制图像输入的也是全连接层，而且这一层的参数众多（CNN参数80%以上））。得到固定长度的特征向量进行分类（全联接层＋softmax输出）不同，FCN可以接受任意尺寸的输入图像，采用反卷积层对最后一个卷积层的feature map进行上采样, 使它恢复到输入图像相同的尺寸，从而可以对每个像素都产生了一个预测, 同时保留了原始输入图像中的空间信息, 最后在上采样的特征图上进行逐像素分类。

##一、Introduction
传统的CNN可以很好的对目标进行分类，但是很难解决某个像素点是属于哪一类的这个问题，终其原因就是因为全连接的时候损失掉了图像的位置信息。

![](http://i.imgur.com/uC6V6Fp.png)

最后进过softmax可以得出对于某一类的概率，因为最后一层的featuremap的激活响应`tabby cat`响应最高，但是这种方法用到分割就捉襟见肘，因为全连接层破坏掉了图片的位置信息，这时候就要想一个办法保存。

最明显的就是所有的卷积操作是不会破坏图片的相对位置信息，也就是通过卷积之后的感受野位置相对不会改变，不可能正立的人，卷积之后的featuremap可视化之后成为倒立的。

##二、Method
论文中的核心idea包括两个部分，一个是全连接到全卷积，另一个是是skip layers的upsampling。

###1.全连接-->全卷积
解决像素级任务的核心。

>将全连接操作转化成卷积操作。也就是卷积最后一层的feature map 如果使用卷积操作是将每个neural Flatten之后dense连接到后面的若干神经元，以alexnet为例，最后一层为256×7×7，得到后面的4096个神经元，但是如果使用7×7的卷积核对前面的featuremap进行继续卷积（padding=0），不也可以得到4096×1×1的向量吗，如果图片大一些，例如384×384，那没alexnet最后一层的大小就是256×12×12，经过一个7×7的卷积核之后就是4096×6×6了，这时候这6×6=36个神经元就有了位置信息。如下图所示。

>![](http://i.imgur.com/4glheLT.png)

>在经过一个上采样的过程，就可以实现一个像素级别的预测了。如下图

>![](http://i.imgur.com/xgPnJui.png)

###2.upsampling
####a. 反卷积恢复图像到输入尺寸就哒溜君来说有两种方式

>1. 对pooling的进行尺寸恢复。这个方法可以通过记录maxpooling的位置，还原pooling之后的结果，然后其他空缺的位置进行差值或者置零。

>2. 反卷积操作。正常的卷积操作是从大的feature map 到小的feature map(如果不进行padding 的话)，所以如果多padding几个像素点，然后同样使用卷积核就可以进行图像的恢复，例如从2×2->4×4，kernel size 如果为3的话padding=2就可以也就是原来的2×2的feature map 变成6×6的，padding的值可以为0也可以是插值。下面这个图可以比较形象的说明这个问题。

>![](http://i.imgur.com/LVeC8Tq.gif)

####b. skip layer
>现在我们有1/32尺寸的featureMap，1/16尺寸的featureMap和1/8尺寸的featureMap，1/32尺寸的featureMap进行upsampling操作之后，因为这样的操作还原的图片仅仅是conv5中的卷积核中的特征，限于精度问题不能够很好地还原图像当中的特征，因此在这里向前迭代。把conv4中的卷积核对上一次upsampling之后的图进行反卷积补充细节（相当于一个差值过程），最后把conv3中的卷积核对刚才upsampling之后的图像进行再次反卷积补充细节，最后就完成了整个图像的还原。

>![](http://i.imgur.com/KPZX7cG.png)

##三、Experiment
实验肯定吊到炸裂，毕竟CVPR 2015 best paper。

由于没有使用全连接，MAC下降明显，所以速度上也是很快的，而且得益于end to end训练

![](http://i.imgur.com/InfdLUn.png)

![](http://i.imgur.com/Q7opUpP.png)

##四、Conclusion
 1.个人感觉这个全连接其实作用不是很大，本身FC就是用来做一个特征拟合的，用在dnn里面，但是CNN这个特征提取的能力太强了，其实完全可以不用FC，直接一个pooling进行输出其实就可以解决问题了。

2.去掉全连接之后，由于位置信息得到了保留，所以可以做很多的是事情，可以怼到bbox做目标检测类似于SSD，也可以上采样做Segmentation，或者深度信息预测，都很有借鉴意义。