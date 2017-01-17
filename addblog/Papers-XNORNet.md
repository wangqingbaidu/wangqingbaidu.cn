title=Papers on Deep Learning(XNOR-Net Binary Convolutional Neural Networks)
en_title=dlp
category=Papers
tags=DeepLearning,Papers,DeepArchitecture
summary=篇论文引入了一种对filter，feature map进行二值化的算法，从而避免了传统CNN中卷积操作的实数乘运算。论文提到，单纯对filter参数二值化，会有2X效率的提升，如果再对feature map的值进行二值化会有58X提升，并提升27X的内存利用率，但是会有一定的准确度损失，但是这篇论文仍然堪称解决CPU训练深度网络效率低的良药。
<ep_info>

#[XNOR-Net ImageNet Classification Using Binary Convolutional Neural Networks](http://arxiv.org/abs/1603.05279)

<font color=red> 本人想把算法思想进行重现，有意愿一起的小伙伴可以联系我，本人qq(邮箱):564326047(@qq.com)，或者直接在下面留言。 </font>

<summary>
##一、Introduction
####A. 相关工作
论文中提到了好几种加速DNN的方法，由于小w精力有限，并没有一一研读，有兴趣的大侠可以自行修行，下面只做一个简单的介绍。
>1. Shallow Network，不使用CNN提取的特征而是使用SIFT等手工特征，但是其他研究者又指出要达到CNN的准确度在参数量上又要相仿，所以要先训练一个DNN，然后模拟这个网络模型。小w认为这样做就印证一句中国的老话，那什么什么，多此一举。CNN最大的特点就是end to end，干嘛非要把人家拆开！；
>2. Compressing pre-trained deep networks，最主要的思想是减少冗余的参数，有些神经元连接的参数就比较小，这种连接在网络中的作用比较小，所以可以去掉，以此来减少冗余运算（神经元之间没有dropout默认是全连接的）；
>3. Designing compact layers，最具代表性的可能就是FCN了，完全不要全连接层；以及使用2个3×3替代一个5×5，这样运算就减少了5*5-3*3*2=7次。 
>4. Quantizing parameters，量化参数，文中指出高精度的参数在提升性能上其实影响不是很大，其实很容易理解，假如一个64位的double参数值为100.5和32位的int的参数值为100，其实在乘以输入之后对于最后的值影响不大，但是在cpu处理起来却是有很大的时间差异。
>5. Network binarization，作者主要对比的方法，后面会做详细介绍

####B. 作者工作
>1. 提出针对weight的Binary Weight方法，将原来的+，-，×，操作，简化成+，-操作。
>2. 结合第一种方法的思想，同时将输入进行Binary Weight，将卷积操作简化到只是用XOR(异或)。

##二、Core Algorithm
先说明一下作者的符号约定，为简化起见，所有的符号仅表示一层的参数（文中作者一层和多层做了区分）：

对于任意一层可以表示为一个三元组`<I, W, *>`其中`I`表示输入，`W`表示这一层的参数，`*`表示实数卷积操作。
####A.Binary Convolutional Neural Network
>1.二值化
>>BCNN的核心idea就是将卷积核的参数二值化，也就是说需要用满足$$I*W ≈ (I ⊕ B) α \quad B∈\{+1, -1\}^{c×w×h}    \quad α∈R^+$$

>>α，B是待求解的参数，接下来就是构造函数，然后最小化这个函数。$$J(B, α)=\|W - αB\|^2$$
>>展开有$$J(B, α) = a^2B^TB - 2αW^TB + W^TW$$
>>由于`B`是二值化的,所以$$n = B^TB$$
>>而且固定值$$c = W^TW$$
>>最后函数转化为$$J(B, α) = a^2n - 2αW^TB + c$$
>>优化这个函数，$$ B^* = argmax_{B}{W^TB} $$ 
>>这个很明显$$B^* = sign(w) \mbox{sign() 为符号函数}$$，然后求导就好了$$a^* = \frac{W^TB^*}{n} = \frac{1}{n}\|W\|_{l1}$$
>>α也就是权重矩阵绝对值的均值

>2.训练
>>在网络前向传播和反向传播的时候使用的是二值化的权重，但是在更新参数的时候，仍然使用的是实数，因为如果权重也成为了了二值化，那么在更新权重的时候会出现梯度消失的情况（因为权重是二值化的，-1，+1），后面的就是CNN的常规套路了。

>>![](http://i.imgur.com/GMlF3AO.png)

>>小w觉得第9行有点问题，因为根据作者的思路，是更新实数weights, 应该是$$\widetilde{W} = UpdateParameters(\widetilde{W}, /frac{∂C}{\widetilde{W}, η_t)$$


####B.XNOR-Networks
>1.二值化
>>方法跟Binary Weights相似，下面直接贴公式了....
>>![](http://i.imgur.com/nLLsG0a.png)
>>![](http://i.imgur.com/58uuszw.png)

>2.训练
>>与前面方法唯一的不同点就是网络的顺序不同。因为如果在pooling之后很可能造成大多数的tensor为+1，所以他吧pooling放在了conv之后。(这一点没想明白。。。),剩下的思路和`algorithm1`一样
>>![](http://i.imgur.com/5L09Xj2.png)

####C.最后贴作者的总体思路
>![](http://i.imgur.com/8Zo4iFS.png)

##三、Conclusion
> ![](http://i.imgur.com/vEcadyN.png)
> 
>最后作者将CPU上的训练速度提升了58X，内存节省了32X，但是性能其实损失是不大的，尤其对于任务相对简单的深度网络，我想应该可以满足最基本的要求。
>
>最后说一点感想，深度学习目前取得的成就各位大侠应该有目共睹，但是为什么深度学习目前已知被雪藏在实验室，或者为什么很难大规模的部署到线上系统上，尤其是没有GPU的实时系统中，很大程度就是受限于CPU的处理能力。小w认为这篇论文为深度学习在普通机器甚至嵌入式设备上使用提供了出路，虽然使用这种二值化的网络会有一定的性能随时，但是如果在性能损失的前提下仍然比传统方法好，而且快，那我们将深度学习应用在工程上，何乐而不为呢？