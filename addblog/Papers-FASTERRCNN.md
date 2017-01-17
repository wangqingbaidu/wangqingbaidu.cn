title=Papers on Deep Learning(Faster R-CNN)
en_title=dlp
category=Papers
tags=DeepLearning,Papers,ObjectDetection
summary=Faster rcnn是用来解决计算机视觉(CV)领域中Object Detection的问题的。经典的解决方案是使用: SS(selective search)产生proposal,之后使用像SVM之类的classifier进行分类，得到所有可能的目标.  使用SS的一个重要的弊端就是：特别耗时，而且使用像传统的SVM之类的浅层分类器，效果不佳。
<ep_info>

[转帖请注明出处www.wangqingbaidu.cn](www.wangqingbaidu.cn)
#[Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks](http://arxiv.org/abs/1506.01497)
不解释了，多快好省地进行目标检测，我只推Faster R-CNN。

##一、Introduction：
Fast R-CNN提供了在目标检测领域的一个baseline，前者包括了对proposal的refine以及对目标的一个分类。但是前者的主要瓶颈就是出现在proposal的选取的过程中。所以目标检测的模型一般包括两个阶段分别是proposal的选取阶段以及一个proposal refine以及classification阶段。

论文主要是针对模型的第一阶段进行的研究，当然也是为了解决由于Fast R-CNN中selective search造成性能下降的问题。作者引入一个RPN（region proposal network）用于提供输入到后端神经网络所需要的proposals，在RPN网络设计时，作者将后端深度网络的参数与前端RPN网络的参数进行共享，实现了一个end to end的网络模型。下图是RCNN模型发展的一个过程。

 ![](http://i.imgur.com/TZJRicw.png)

由于使用端到端的模式训练proposal生成模型，所以proposal的生成质量一般很高，作者实验中使用RPN网络的top-100与top-6000的proposal分别输入到后端，最后只有百分之一的精度差距，其RPN网络提取的proposal精度可见一斑。当然也是因为生成的候选区域量少，所以运行效率也非常高（相比于前面的工作）。

##二、Related Work:
区域检测前面的工作已经做了很多，比较有代表性的就是SPPnet，以及Fast R-CNN，但是他们在前期候选区域生成的时候都存在着性能瓶颈。这个瓶颈一般是由于proposal的选取一般都是在cpu上进行，并不能很好地整合到深度网络中（一般使用gpu加速）。

目标检测的两个阶段：

>第一阶段的候选区域生成一般集中在两个方法，一个是基于超像素的，eg. Selective Search，CPMC， MCG，另一个是基于滑动窗口的, eg. EdgeBoxed.
>
>第二阶段的工作由R-CNN提供baseline，但是它只是负责分类任务，并不负责对box的调整，所以它的准确度也就局限在了候选区域的生成阶段。当然后面的很多文章就围绕在将怎么对bounding box进行调整上面。

最后，Faster R-CNN = RPN + Fast R-CNN(without ss)

##三、RPN(Region Proposal Network):
RPN的核心思想是使用卷积神经网络直接产生region proposal，使用的方法本质上就是滑动窗口。

>在卷积的最后一层（一般是60，40左右的长宽），通过一个3*3的卷积核与每个特征图进行卷积，这个3*3的卷积核以（2,2）为半径一共可以生成9个anchor。这9个anchor在返回原图像时可以对应到不同面积以及不同尺度的感受野。anchor如下图

 >![](http://i.imgur.com/EmpciAM.png)

>所以最后会输出40*60*9≈2w个proposal，由于这些proposal会有很多的重叠，所以为了提高运行效率作者同样使用了非极大值抑制的方法对其进行剪枝。

>对于每一个proposal，对最后一层的feature map来说会生成256维的一个特征向量（256的取值取决于卷积最后一层的filter的个数），然后将这个特征向量分别扔给分类模型（二分类模型，用于区分是否为背景），回归模型（用于proposal的refine）。

>在分类层中会得到每个proposal是否是目标区域（不区分类别）的概率。最后根据region proposal得分高低，选取前X个region proposal，作为Fast R-CNN的输入进行目标检测。

##四、Loss Function
损失函数分为两个部分，分别是分类损失和回归损失，对应于RPN输出的那两层
 
$$loss = L(\{p_i\},\{t_i\})=\frac{1}{N_{cls}}\sum_i L_{cls}(p_i,p_i^*) + \lambda \frac{1}{N_{reg}}\sum_i p_i^* L_{reg}(t_i,t_i^*)$$

前面的N和λ是用来做归一化的。

分类的样本根据覆盖率进行数据的标记，当覆盖率达到0.7以上时为正样本，低于0.3时是负样本，其他的比例不用再训练。

Bounding box的回归损失依据的是R-CNN[1]论文中的损失。

##五、Training
参数共享的方法：

>alternating training首先训练RPN, 之后使用RPN产生的proposal来训练Fast-RCNN, 使用被Fast-RCNN tuned的网络初始化RPN, 如此交替进行

>joint training首先产生region proposal, 之后直接使用产生的proposal训练Faster-RCNN，对于BP过程, 共享的层需要combine RPN loss和Faster-RCNN loss

训练分为4个步骤：

>1)	使用在ImageNet训练的模型初始化RPN网络参数，微调RPN网络；

>2)	使用(1)中RPN网络提取region proposal训练Fast R-CNN网络，也用ImageNet上训练的模型初始化该网络参数；（现在看来两个网络相对独立）

>3)	使用(2)的Fast R-CNN网络重新初始化RPN, 固定卷积层进行微调，微调RPN网络；

>4)	固定(2)中Fast R-CNN的卷积层，使用(3)中RPN提取的region proposal对Fast R-CNN网络进行微调。

##六、Experiments

 ![](http://i.imgur.com/RDsGj4E.png)

##七、Conclusion

1)	end2end的网络确实要比人工选取的那些proposal的方法要准确的多，所以后面要在准确率上有所提升还是要想办法将任务的目标整合到端到端的网络中去，就跟前面所说的DNDF[2]。

2)	RCNN其实用到各种任务中，可以提高不同任务的准确度，通过RCNN跑出来的结果，将该部分的图片剪切出来，然后在进行特征任务的学习。

##八、Reference

[1] R. Girshick, J. Donahue, T. Darrell, and J. Malik, “Rich feature hierarchies for accurate object detection and semantic segmentation,” in IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2014.

[2] Kontschieder P, Fiterau M, Criminisi A, et al. Deep Neural Decision Forests[C]// IEEE International Conference on Computer Vision. IEEE, 2015:1467-1475.
