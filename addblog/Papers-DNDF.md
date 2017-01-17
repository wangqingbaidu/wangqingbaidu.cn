title=Papers on Deep Learning(Deep Neural Decision Forests)
en_title=dlp
category=Papers
tags=DeepLearning,Papers,DeepArchitecture
summary=Deep Neural Decision Forests为ICCV2015 Best Paper，这篇论文提出了一个非常有建设性的思路，那就是将传统数据挖掘（分类、回归超牛逼）的思想结合到卷积神经网络（提特征超牛逼）里面，这样训练出一个end to end的模型。
<ep_info>

#[Deep Neural Decision Forests](http://159.226.251.229/videoplayer/ICCV15_DeepNDF_main.pdf?ich_u_r_i=797f17ed493abb53dc4505786ba4e3d9&ich_s_t_a_r_t=0&ich_e_n_d=0&ich_k_e_y=1645098914750763572491&ich_t_y_p_e=1&ich_d_i_s_k_i_d=7&ich_u_n_i_t=1)
当小w还是一名研一的小学生时，就对所谓的数据挖掘十分感兴趣，当时就想，通过这个玩意就能让机器知道连我都不了解我的东西，确实十分神奇。奈何研二导师离职（是不是很悲剧。。。），就到隔壁组去做深度学习了，哎~，发现深度学习竟然比数据挖掘更吊。。。（因为以前认知的数据挖掘都要自己去提取特征然后扔给`RF`,`SVM`等等，但是`CNN`完全End2End连提特征的任务都省了）

当做了一段时间就发现，其实他们还是有很多相关性的，或者说其实`CNN`到最后还是用到了数据挖掘的那些模型。举个简单的例子，一般`CNN`最后跟的就是若干个（一般2个）全连接，这就是普通的`DNN`啊，当用使用别的分类器替换时 eg. `SVM`，这样就变成了一个线性分类器，好像效果比FC有提升。

所以就在想一个问题，就是能不能把这个`CNN`与其他的通用模型结合起来搞事情，而这篇论文就提供了一个很好的思路。 `CNN`+`DT`, 卷积神经网络提供特征，决策树（森林）提供分类。


##一、Background
既然是Decision Forest，那么就要先知道什么是`决策树`、`回归树`、`随机森林`。

>A. 决策树：大多是用来分类的。选择分类属性的标准是信息增益最大（Information gain），涉及到熵这个概念（The Shannon entropy）。公式如下，h(s)表示node s的熵，信息增益则是node s的熵减去它的左右子节点的熵。如果信息增益为正，则说明这是一个好的分裂split。 

>The Shannon entropy:
>
>$$h(s)=-\sum p_y*log(p_y) where y\in \{1,2...k\}$$
>
>Information gain:
>
>$$I_j=H(s_j)-\frac{s_j^R}{s_j}H(s_j^R)-\frac{s_j^L}{s_j}H(s_j^L)$$
>
决策树的构造方法： 从根节点开始， 
>>a.N个M维的样本，那么共有（N-1）*M种splitting options可以将其分裂
> 
>>b.根据information gain的原则选择最大增益的splitting option进行分裂
> 
>>c.分裂到子节点后，重复1-3直至停止条件（停止条件一般包括Max depth, min info-gain, pure(节点已经分类纯净), max count of node）

>B. 回归树：顾名思义就是来做回归的，选择变量的标准用残差平方和。熟悉通常意义的回归分析的人，一定知道回归分析的最小二乘解就是最小化残差平方和的。在回归树的根部，所有的样本都在这里，此时树还没有生长，这棵树的残差平方和就是回归的残差平方和。然后选择一个变量也就是一个属性，通过它进行分类后的两部分的分别的残差平方和的和最小。然后在分叉的两个节点处，再利用这样的准则，选择之后的分类属性。一直这样下去，直到生成一颗完整的树。 
>
>C. 随机森林：是用随机的方式建立一个森林，森林里面有很多的决策树组成，随机森林的每一棵决策树之间是没有关联的。在得到森林之后，当有一个新的输入样本进入的时候，就让森林中的每一棵决策树分别进行一下判断，看看这个样本应该属于哪一类（对于分类算法），然后看看哪一类被选择最多，就预测这个样本为那一类。

##二、Introduction
先传达一个重要的思想：翻译成中文也很简单，就是你深度学习这么牛逼就是因为你把提特征和具体问题揉到了一起，搞e2e（end to end）。
><font color=red>One of the consolidated findings of modern, (very) deep learning approaches is that their joint and unified way of learning feature representations together with their classifiers greatly outperforms conventional feature descriptor & classifier pipelines, whenever enough training data and computation capabilities are available.</font>


>因为作者在做的将数据挖掘方法与CNN端到端结合的方法比较有原创性，所以相关工作介绍不多，最主要是与

>[Globally Optimal Fuzzy Decision Trees for Classification and Regression](http://cse.hcmut.edu.vn/~chauvtn/data_mining/Reading/Chapter%204%20-%20Classification/1999%20Globally%20optimal%20fuzzy%20decision%20trees%20for%20classification%20and%20regression.pdf)

>主要的区别有三个方面
>
>>a. We provide a globally optimal strategy to estimate predictions taken in the leaves (whereas former simply uses histograms for probability mass estimation). 
>
>>b. The aspect of representation learning is absent in former 
>
>>c. We do not need to specify additional hyper-parameters which they used for their routing functions (which would potentially account for millions of additional hyper-parameters needed in the ImageNet experiments).

##三、Global Architecture
FC之前输入的是`CNN`的特征，接下来的dn为Decision Nodes，πn为Prediction Nodes。

其实这个结构可以换个角度理解，我们最常见的就是2层的全连接层，只不是现在换成了决策森林；各位大侠再仔细观察这个决策树，其实可以看成是若干层全连接层`dropout`了一些指定的连接，也就是极稀疏的全连接层（因为虽然是决策树，但是同样每一个节点在输出之后都会有一个激活函数，文中采用的是`sigmoid`函数）

当给定x时，对样本的预测为

$$\mathbb{P}_T[y|x,\Theta ,\pi ]=\sum _{\mathit{l}\in \boldsymbol{L}}\pi_{\mathit{l}_y}\mu _\mathit{l}(x|\Theta)$$

ok，下面说一下符号的意义:

Decision nodes indexed by `N` are internal nodes of the tree, while prediction nodes indexed by `L` are the terminal nodes of the tree. Each prediction node l∈L holds a probability distribution πl over Y.

`l↙n`, `n↘l`分别表示当前决策节点向左路由和向右路由
![](http://i.imgur.com/pZwIXOI.png)

---
![](http://i.imgur.com/dMXvdYa.png)

##三、Decision Tree with Stochastic Routing
本文的这个决策树并不是向传统意义上的决策树，传统的决策时是二值的，也就是在每个节点划分数据之后（根据特征的最大熵增益），对后面的划分就不会有任何影响，但是本文的决策树使用的是<font color=red>概率决策树</font>，当然这也是它与 _[Globally Optimal Fuzzy Decision Trees for Classification and Regression](http://cse.hcmut.edu.vn/~chauvtn/data_mining/Reading/Chapter%204%20-%20Classification/1999%20Globally%20optimal%20fuzzy%20decision%20trees%20for%20classification%20and%20regression.pdf)_最大的区别。

>A. Decision nodes && Forest
>
>$$d_n(x;\Theta)=\sigma (f_n(x;\Theta)) $$
>
>`σ`是`sigmoid`函数，每一个决策节点之后都要经过这个激活函数，`f`为一个输入维度到一维实数空间的一个映射即X→R.
>
>$$\mathbb{P}_{\boldsymbol{F}}[y|x]=\frac{1}{k}\sum_{h=1}^k\mathbb{P}_{T_h}[y|x]$$

>B. Learning Trees by Back-Propagation
>论文中的loss还是使用的是-log损失，对于整个batch的损失函数为
>$$R(\Theta, \pi;\mathfrak{T})=\frac{1}{\mathfrak{T}}\sum_{(x,y)\in \mathfrak{T}}L(\Theta,\pi;x,y)$$
>$$L(\Theta,\pi;x,y) = -log(\mathbb{P}_{\boldsymbol{T}}[y|x,\Theta,\pi])$$
>
>loss函数的梯度为：
>
>$$\frac{\partial L}{\partial \Theta}(\Theta,\pi;x,y)=\sum_{n\in N}\frac{\partial L(\Theta,\pi;x,y)}{\partial f_n(x;\Theta)}\frac{\partial f_n(x;\Theta)}{\partial \Theta}$$
>
>$$\frac{\partial L(\Theta,\pi;x,y)}{\partial f_n(x;\Theta)}=d_n(x;\Theta)A_{n_r}-\bar{d_n}(x;\Theta)A_{n_l}$$
>
>f为任意定义的关于Θ的函数，好比说`f = Θx+b`
>C.Learning Prediction Nodes
>预测节点时线下更新的（非bp进行参数更新），并且预测节点时按照每一个batch进行数据更新的。
>
>$$\pi_{l_y}^{t+1} = \frac{1}{Z_l^{(t)}}\sum_{(x,y') \in T}\frac{\textrm{1}_{y=y'}\pi_{l_y}^{(t)}\mu_l(x|\Theta)}{\mathbb{P}_{\boldsymbol{T}}[y|x,\Theta,\pi^{(t)}]}$$

>D.Algorithm
<pre class="brush:cpp;">
Require: T : training set, nEpochs
random initialization of Θ
for all i∈{1....,nEpochs} do
	Compute π by iterating (11)
	break T into a set of random mini-batches
	for all B: mini-batch from T do
		Update Θ by SGD step in (7)
	end for
end for
</pre>

##四、Experiments
结果不用多说，肯定很牛逼（但是现在的ResNet，GoogLeNet(V几忘了)什么的已经超过他了），但是有一个点想要跟各位大侠分享一下的就是：

![](http://i.imgur.com/UVQAHaM.png)

因为小w项目组需要对数据进行划分，然后进行分布式检索，由于现在所有的库数据时加载到每一个节点的，但是这很明显是有冗余的，所以最好是能把数据很好的划分开，举个例子，如果一个检索任务能够以很高的概率出现在一个节点，我就不用把这个检索任务发送到其他的节点了，这样就可以极大的提高吞吐效率。

论文中提供了一个思路就是，我可以控制路由到每个叶子节点的数据，也就是随着训练epoch的增加，数据会以很高的概率路由到指定的节点，当然这也是本文作者希望去做的一件事情。

##五、Conclusions
其实这篇论文之所以能够成为Best Paper很大程度上是开创了将传统数据挖掘的模型，放到深度网络里面去进行端到端的学习，因为传统模型的拟合能力非常强，但是需要人工提取一些非常强力的特征，而`CNN`又以其超强的图片特征提取能力而著称，所以这两个方向的结合就会擦出不一样的烟火。

其实这种传统方法与深度学习结合是一个很值得做的方向，但是最主要是怎么将传统的模型或者方法放到端到端的模型中去，这是很值得研究的。而这篇论文就提供了一个方向。