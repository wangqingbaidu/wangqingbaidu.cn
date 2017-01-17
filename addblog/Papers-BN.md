title=Papers of Deep Learning(Batch Normalization)
en_title=dlp	
category=Papers
tags=DeepLearning,Papers,ComonTricks
summary=Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift. 使用BN正则化之后的网络可以拥有更高的learning rate, 可以减少drop out的限制，或者不使用drop out。而且由于正则化之后相应的lr的提高，可以极大的减少训练的时间。
<ep_info>

#一、Introduction
在深度学习中，bp经常使用的方法SGD来对loss进行最优化。通过调整mini batch的loss来逼近整个训练集上的最优解。相对于单个训练样本进行bp，使用mini-batch有2个好处：
>1. 用mini-batch相比之下可以更好的模拟整个训练集上的loss，因为数据比单个有更强的表达能力。
>2. 使用mini-batch可以更适应GPU上进行并行计算。

但是在训练整个网络的过程中会出现几个问题
>1. 虽然梯度下降很有效果，但是在模型的训练过程中有很多的超参需要设计，最重要的就是lr，由于参数之间会一层层的影响，所以这个值一般都会设置的比较小，这样才能防止前面层一个很小的修改导致后面参数出现爆炸，当然也不能太小，这样就会在bp的过程中出现梯度消失。所以这些参数的设置很大程度上依赖于经验值，但是经验值这个东西有的时候是很不靠谱的。

>2. 同时，输入的分布变化是比较频繁的，这样当一个训练样本训练完成之后，bp修改完参数，下一个样本由于分布不同，需要在此修改参数。这样就会造成很大的浪费。

>3. 由于激活函数的原因很可能陷入局部最优而无法自拔。这就是为什么ReLU会出现来替代tanh和sigmod(其实并没有替代而是提供一个更多的选择)

>4. 正则化可以一定程度上解决上面的问题，但是以往的梯度下降没有考虑到正则化系数的优化。

#二、Batch-Normalization
文中对问题进行了2个简化
>1. Normalize each scalar feature independently（也就是每一个维度，看作是独立的）
>2. Each mini-batch produces estimates of the mean and variance（每一个mini-batch都有自己的均值和方差）

最后就是文中最主要的2个算法以及bp参数修改的过程

>![](http://i.imgur.com/d1ywxv9.png)

上面的算法是将X，也就是featuremap的每一个维度进行初步的正则化

>![](http://i.imgur.com/2umP3gW.png)

调整每一个mini-batch的均值和方法，进行输出

>![](http://i.imgur.com/9M3za06.png)

这是训练过程中bp修改参数的公式。

#三、Conclusion
这篇论文经过将每一个输出到激活函数的x进行正则化之后可以减少分布对魔性训练带来的影响。经过正则化之后的输出可以拥有更大的lr以及不那么依赖dropout，而且可以极大的减少训练的时间。

当然这个方法最主要的不是提高模型的精度，虽然在使用BN之后有一定的提升，但是使用上最主要还是提高训练的效率。