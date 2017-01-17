title=Papers on Deep Learning(Deep Embedding with Contextual Evidences)
en_title=dlp
category=Papers
tags=DeepLearning,Papers,ImageRetrival
summary=使用基于SIFT的局部特征以及基于CNN提取的全局特征对图片进行索引。文中提到SIFT局部特征在图片检索领域具有里程碑式的影响，但是受限于其局部而没考虑到全局的线索，由此带来了mAP的损失，虽然后面的研究工作也提出了基于color和boundary的特征，但这些都是启发式的，没有理论依据。因此作者提出了使用CNN的region以及global特征来弥补SIFT的不足，同时针对这3中特征建立索引称之为Deep Embedding。（不知道作者哪里来的胆量，批判人家没有理论依据，说得好像CNN有什么理论依似的。）
<ep_info>

#Seeing the Big Picture:Deep Embedding with Contextual Evidences
使用基于SIFT的局部特征以及基于CNN提取的全局特征对图片进行索引。文中提到SIFT局部特征在图片检索领域具有里程碑式的影响，但是受限于其局部而没考虑到全局的线索，由此带来了mAP的损失，虽然后面的研究工作也提出了基于color和boundary的特征，但这些都是启发式的，没有理论依据。因此作者提出了使用CNN的region以及global特征来弥补SIFT的不足，同时针对这3中特征建立索引称之为Deep Embedding。（不知道作者哪里来的胆量，批判人家没有理论依据，说得好像CNN有什么理论依似的。）
##一、Introduction
####A. 相关工作
>1. 里程碑意义的SIFT局部特征；
>2. BoW + 倒排索引，加快检索速度；
>3. CNN近几年屌得不要不要的。

####B. 以前工作的缺陷
>1. SIFT只关注局部特征，对上下文特征描述的力度是不足的；
>2. 基于color和boundary的特征是启发式的，没有理论依据；
>3. CNN在Classification和Object Detection上很牛逼，但是很少用在图片检索上面。

####C. 作者工作
>1. 将CNN全局特征与SIFT局部特征结合起来；
>2. 提出一个概率模型，来判断keypoint是否真的match。

##二、Feature Design
首先先明确作者的一个基本理念：SIFT作为`local`特征，CNN提取的特征作为`region`和`global`特征。而作者说的`True Match`指的是三者(`local`, `region`, `global`)都匹配才是`True Match`。

其次作者使用`environment`代表`region`,`global`特征。同时使用的是已经训练好的CNN模型进行特征提取，该模型是[Decaf](http://arxiv.org/abs/1310.1531)

`local`特征就不说了，就是SIFT特征，`global`特征就是一张训练图片通过CNN的特征。
####A. `region`特征
>作者将图片的`region`特征定义为两个图片的划分，分别是4X4和8X8的区块。
>
>这里所有的区块应该都是被剪切下来之后当做一张完整的图片(当然要进行resize)输入到CNN的。

>![](http://i.imgur.com/QrDFVF2.png) 

####B. 一些问题
>1. 作者发现，CNN提出来的特征的数值差异十分的大[-72.8, 24.8]，作者认为：这么大的差距可能造成单一维度的巨大差异而使后面的欧氏距离偏差很大，其实有时候某一个维度的决定性不应该对维度产生这么大的影响。所以作者使用了一个叫做SRN(Signed Root Normalization)的正则化。$$f(x) = sign(x)|x|^α$$
>α为可变参数，经试验，α=0.5效果较好。
>2. 特征编码，使用LSH对特征进行二进制编码，具体操作参见[LSH](https://www.baidu.com/s?wd=%E5%B1%80%E9%83%A8%E6%95%8F%E6%84%9F%E5%93%88%E5%B8%8C)

##三、Deep Embedding Framework
经过两个公式的推导，得出概率模型。
>
>####f(x, y) = p(y ∈ Tx)
>
>![](http://i.imgur.com/FTfpTX3.png)
>
>x,y分别代表查询和索引的两个keypoint， Tx为x的`True match` keypoint的集合, y∈Tx(后面记为Tx)，ξ为x，y的上下文特征。由于`True Match`的定义后项为0。所以推导出下面公式：
>
>![](http://i.imgur.com/4Y50WYY.png)
>
>此公式是由上面的公式利用贝叶斯定理得出的。作者将公式拆分为3各部分(用`·`分割的)


####A. Term 1
>![](http://i.imgur.com/5sPO9O6.png)
>
>简化为`local`特征的相似度，dH为海明距离，σ为参数，κ为海明距离的阈值，根据以前的经验，作者设置为60。

####B. Term 2
>![](http://i.imgur.com/8cVgsZl.png)

>`region`特征相似度，dE为欧式距离，γ为参数，后面作者会比较使用LSH编码和不使用LSH编码的mAP。

####B. Term 3
>![](http://i.imgur.com/blxzwfl.png)

>`global`特征相似度，dE为欧式距离，θ为参数，后面作者会比较使用LSH编码和不使用LSH编码的mAP。


##四、Deep Indexing
####A. 传统索引
传统的倒排索引是将所有的特征都发入到倒排表中，如图，由于使用到了`region`和`global`特征，会存在一个`region`和`global`特征对应多个keypoint的情况，这样会造成内存空间的巨大浪费。

> ![](http://i.imgur.com/QqUqVL9.png)

####B. 索引优化
作者将索引的共同部分取出，使用一个指针，指向公共的特征部分，结构如图

>![](http://i.imgur.com/MsxcB7X.png)

####五、Experiments
当然是各种屌(这很正常，使用了更多的特征)，下面贴出几个结果截图。

####A. σ, γ, θ参数

>![](http://i.imgur.com/zF0ZLbR.png)

####B. mAP

>![](http://i.imgur.com/8kOTwnn.png)

##六、Conclusion
虽然作者但是在holiday的数据集上取得了state-of-art, 但是个人感觉想法比较简单，抱了一把CNN的大腿，毕竟14年的文章。

但是这个想法在工业界应该可以使用，毕竟工业界对效率的要求大于性能，而且工业界可以不用SIFT提取特征，如果使用仅用`global`特征和`local`特征，应该可以在ms级完成检索，同时有一定效率的提升。