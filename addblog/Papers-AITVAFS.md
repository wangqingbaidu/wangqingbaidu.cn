title=An Introduction to Variable and Feature Selection
en_title=dm	
category=Papers
tags=DataMining,FeatureSelection
summary=这篇文章应该算是特征筛选领域一篇非常非常屌的综述了，在度娘的学术引用量已经达到了6600+，其涵盖面之广可见一斑。但是小w发现这么牛逼的文章，竟然没有翻译或者几篇相关的blog，感觉也是日了狗了。小w一狠心一跺脚就决定吃了这个螃蟹。
<ep_info>

#[An Introduction to Variable and Feature Selection](http://dl.acm.org/citation.cfm?id=944968)
小w由于最近忙于找工作，小w的好多小伙伴反应好多面试官喜欢问是不是了解特征选取？what？小w致力于cnn500年怎么可能了解这些东西（CNN是没有特征选取的，因为它所有的特征都是end-to-end学出来的），但是出于好奇还是忍不住决定看看这个号称玄学的东西。
##一、Introduction
文章的引言就是扯一下这些年特征的维度怎么从几十维一下子到了成百上千维，而且说这个特征选取工作如果一个个弄是多么np的一个问题，所以没讲什么valuable的东西，但是还是传达出一个重要的点就是对于有些模型来说（线性模型，等），特征选取是十分重要的（当然像什么xgb可以随便加特征结果总不至于变坏，但是会有性能的损失），同时筛选之后的特征可以增加对原始数据的理解等等。

####文章将特征筛选分成了3类，分别是`filter`, `wrapper`, `embedded method`。后面会做详细介绍

在引言最后的10条可以说是数据挖掘的princeple还是很有指导意义的。
>![](http://i.imgur.com/hioTabT.png)

##二、Filter
`filter`一般作为一个baseline的形式存在，通过`filter`之后的特征会有一个明显的维度的下降，将这些降维后的`feature`(文章不区分`feature`和`variable`) fit 给那些线性或者非线性分类器会有一个提升。
###1.Variable Ranking
>其实他的思想是很简单的——选取最有用的那些特征，去掉没用的特征，就像吉姆·柯林斯在他的《从优秀到卓越》一书中写的，请对的人上车。那问题来了怎么去rank这些特征呢？
>
>下面先说明一下文章中常用的符号
>
>$$x_{k,i}, y_k, cov, var$$
>
>分别表示输入X的第k个样本的第i列特征，点k个样本的label信息，协方差，方差。后面大写的表示数据的全集，小写的是样本。
>用来对衡量变量的rank作者使用的是Correlation Criteria，用下面这个公式表示
>
>$$R(i)= \frac{cov(X_i, Y)}{\sqrt{var(X_i)var(Y)}}$$
>
>关于协方差的性质大家可以自行[百科](http://baike.baidu.com/link?url=C9yzKVmse_7IIYVXNwLMf4aAOGCFYLFkDUDNolZc8CSiqbLrHegpfdp907MstHIoipIJtXk3jj5eLFHUdJi4qK)，小w相信各位大小一看就理解了，就不再赘述。
###2.Information Theoretic Ranking Criteria
>这个理论有点类似于`熵`的形式，用来描述variable X概率分布和Y概率分布的依赖性。
>
>$$I(i)=\int _{x_i}\int _y p(x_i,y)log\frac{p(x_i,y)}{p(x_i)p(y)}dxdy$$
>
>由于真实的概率分布我们是无法知晓的，所以上面的积分形式我们是无法实现的，只能通过sample来进行估计
>
>$$I(i)=\sum _{x_i}\sum _y p(X=x_i,Y=y)log\frac{p(X=x_i,Y=y)}{p(X=x_i)p(Y=y)}$$
>
>由于这个sum依赖于X，y个数，如果都比较大，所以一一的穷举显然是不靠谱的。
###3.Problems
>显然通过这种标准进行的特征筛选是有问题的，由于所有的筛选标准都采用的单个特征进行，所以忽略了一些上下文的信息。虽然可能某几个特征是没有用的，但是如果综合考虑了他们的组合，有事就能取得比较好的分类效果。
>
>看下面的例子。
>
>![](http://i.imgur.com/oDs7XNf.png)
>
>还有就是就算`R(i)`和`I(i)`比较高，但是可能较高的几个特征是线性相关的，所以相关性不能考虑到特征的冗余。
>下面给各位大侠贴一下作者在文中大写加粗的结论，还请各位大侠自己体会。
>>a. Noise reduction and consequently better class separation may be obtained by adding variables that are presumably redundant.
>
>>b. Perfectly correlated variables are truly redundant in the sense that no additional information is gained by adding them.
>
>>c. Very high variable correlation (or anti-correlation) does not mean absence of variable complementarity.
>
>>d. A variable that is completely useless by itself can provide a significant performance improvement when taken with others.
>
>>e. Two variables that are useless by themselves can be useful together.

##四、Wrapper && Embedded
>`wrapper`是通过选取特征的一个子集，然后用这个子集训练一个新的模型，通过模型的loss来选择是否用这个子集。当然每次都需要重新训练一个模型是很耗费资源的，所以一个好的子特征选取的策略是必须的。但是`embedded`方法则是将特征选取的工作融合到了模型当中，当然你需要知道怎样去定义这样的一个特征选取器。

###1.Nested Subset Methods
文中给出了3种`Nested Subset`的方法，`s`为特征的个数，`J(s)`为`objective function目标函数`，到底`loss function`, `cost function`, `objective function`有什么区别大家可以参考一下[这个解释](http://stats.stackexchange.com/questions/179026/objective-function-cost-function-loss-function-are-they-the-same-thing)，我这里只把最后的结论给大家。
>
>     Loss function is a part of a cost function which is a type of an objective function
>
>>1.Finite difference calculation: The difference between J(s) and J(s+1) or J(s−1) is computed for the variables that are candidates for addition or removal.
>
>>2.Quadratic approximation of the cost function
>
>>3.Sensitivity of the objective function calculation
>
>第一种方法应该比较好理解，就是每次增加一个或者减少一个特征，然后看这个目标函数的变化，变好则证明增加/删除的特征好，反之则差。这个地方如果对于线性model来说的话，可以不必要每次重新训练。
>
>个人感觉第二种和第三种方法的差异性不大，都是通过梯度来优化这个目标函数，可能最大的区别就是第二种方法使用`backward elimination`, 而第一种方法使用的是`forward selection`。

###2.Direct Objective Optimization
>从名字可以很清楚的看出来啊，就是直接优化特征的选择，这个方法主要就是集中在了`norm`上面，关于norm regularization，大家可以参考一下这几篇blog
>> [http://blog.csdn.net/zouxy09/article/details/24971995/](http://blog.csdn.net/zouxy09/article/details/24971995/)
>
>>[https://rorasa.wordpress.com/2012/05/13/l0-norm-l1-norm-l2-norm-l-infinity-norm/](https://rorasa.wordpress.com/2012/05/13/l0-norm-l1-norm-l2-norm-l-infinity-norm/)
>
>>[http://www.chioka.in/differences-between-l1-and-l2-as-loss-function-and-regularization/](http://www.chioka.in/differences-between-l1-and-l2-as-loss-function-and-regularization/)
>
>这几篇blog讲的很详细了，就不再赘述，总而言之就是`l1`制造了稀疏性，所以可以做特征选择，而`l2`更适合用来防止过拟合。

#五、Feature Construction and Space Dimensionality Reduction
前面的几种方法都在介绍各种特征的筛选，这些方法都是导致了一些特征直接就被扔掉了，但是难道这些被扔掉的特征真的都没有用吗？其实不然，中国的有句老话不就是三个臭皮匠赛过诸葛亮吗。所以即使某些特征的表现能力比较弱，但是多个这种特征糅合在一起是不是就会好呢？答案是肯定的。
###1.Clustering
>聚类的方法博大精深，由于我不是搞聚类的，所以就不在各位大侠前面班门弄斧，所以有兴趣的童鞋可以去专门找一些聚类的文章读读。这里我就举一个我切实的例子好了。
>
>>小w不是刚做完阿里音乐的比赛吗，其中第一赛季还是套路就是提特征然后跑模型，其中小w负责的那个部分就是用户的特征，用户听歌其实有很多种类，包括喜欢听那些歌手，喜欢什么时间听等等，拿用户喜好时间举例，用户听歌分布在一天的24个小时，所以小w进行了24维的one-hot encoder，但是这24维的特征表现效果就很差，但是当把这些特征聚类分成上午，下午，晚上，深夜等表现就有所提升。
>
>所以小w想说的就是这种事情其实还是考察我们对数据的理解，而不单单是聚类这么简单。如果数据理解都不清楚的话，你对哪几类进行聚类呢？
###2.Matrix Factorization
>这个矩阵分解就略显奇妙了，像现在常用的SVD，LDA等等，确实在降维上面有很好的表现，所以各位大侠在做挖掘的时候可以进行考虑。这个矩阵分解就不再介绍了，这些技术已经很成熟，大家可以自行谷哥or度娘。

#六、Conclusion
作者最后提出了一些非常开放性的问题，大家有兴趣的可以去研读一下。小w个人感觉，这种东西仁者见仁智者见智，没有统一答案，又是那句老话，实践是检验真理的唯一标准。

最后其实我想说就是，特征选择是数据挖掘的前面的一部分，为的就是帮助我们更好的理解数据亦或是让模型取得更好的效果。所以这个东西最好是在模型前面使用， 举个例子，就是一个线性SVM(l1 norm)模型进行特征选择，然后把这些选好的特征扔给像nn或者xgb这种模型，效果一般会有不过的提升。