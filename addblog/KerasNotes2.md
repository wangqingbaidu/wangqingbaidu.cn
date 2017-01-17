title=Keras深度学习框架学习笔记
en_title=kerasNotes
category=DeepLearning
tags=DeepLearning,Theano,Keras
summary=modal加强版。本文给大家继续安利Function API，发现简直太强大了，推荐各位太君不要使用Sequential，直接上FAPI这完全可以搞定所有的网络结构，无论你是并行还是参数共享还是balabala...
<ep_info>

#三、Functional API
Functional API(下称FAPI)实现了模型的大一统，也就是Sequential Model可以做的他都可以做。

###它的核心思想就是：<font color=red>所有model都是可调用的(All models are callable, just like layers)</font>

首先是所有的layer或者model都是可调用的，如果十分熟悉python的童鞋一定知道`__call__`这个内部函数，如果你实现了这个参数，那么这个类就可以被当成函数一样调用，如果去看Keras源码或者自己实现一个自定义的layer的话，`call`函数是Keras要求必须要实现的（为什么是`call`而不是`__call__`,我想应该是`compile`函数在起作用，具体是不是等看完源码再分享给大家）。

其次就是layer的无差别对待，其实这是很容易理解的，因为无论你是layer还是model输入是tensor输出也是tensor，这些东西其实在Keras看来无差别的，所以FAPI可以无差别的对待。

##1. Example
	
>>     model = any_sequentail_model
	x = Input(shape=(784,))
	y = model(x)

>如果是sequence input也很好办

>>     input_sequences = Input(shape=(20, 784))
	processed_sequences = TimeDistributed(model)(input_sequences)

> 这样就可以实现时序的输入。


##2. Multi Input

>大家在读论文的是时候很多情况下并不是一个简单的模型在跑，而是多个模型同时跑，然后进行伟大的模型融合或者层参数的共享，这时候就会用到多输入。

> ###a.Merge
> 这是多输入问题中经常会碰到的，就想下面的这个情况，两个输入同时输入到merge_1 层
> ![](http://i.imgur.com/JBoyqTU.png)
> 
> 这时候最好的办法就是使用Keras的多输入。使用起来也十分的简单：
>      
>>      `x = merge([lstm_out, auxiliary_input], mode='concat')`
>
><font color='red'>tips </font>: `mode`可以取值`sum`, `mul`, `concat`, `ave`, `join`, `cos`, `dot`你能想到的第一个意思可以mode没跑了。
>
>紧接着就可以把x当成普通的层的输出进行使用。

> ###b.Share
>这个share和merge有所不同，merge是将输入进行组合之后然后输入，share是多个输入同时共享一个层，虽然都是有多个输入，但是他们对layer的理解确实千差万别。

>>     tweet_a = Input(shape=(140, 256))
	tweet_b = Input(shape=(140, 256))
	# this layer can take as input a matrix
	# and will return a vector of size 64
	shared_lstm = LSTM(64)
	
>>     # when we reuse the same layer instance
	# multiple times, the weights of the layer
	# are also being reused
	# (it is effectively *the same* layer)
	encoded_a = shared_lstm(tweet_a)
	encoded_b = shared_lstm(tweet_b)

>多个input同时share一个层的时候，如果没有merge就会有多个output（除非丢弃）。

##3.Model 
>###a.Construction
>`model = Model(input=[input_a, input_b], output=output)`
>
>输入就是单输入和多输入的输入，输出为经过若干层之后的输出。当存在多输入的时候，如果没有merge，那么就需要对每一个输出建立一个model，并且进行相应的compile。本代码样例中是对input进行了merge。

>理解模型的建立其实很简单，就是我这个输出（肯定是单输出）需要用到什么输入，我对应的input参数就是包括哪些输入。

>###b. Compile
>模型的编译跟`Sequential`是一样的。但是有一点要补充的是由于有多输出的问题，所以可以通过`name`属性定义的名字，对每一个输出采用特定的loss func。同时也可以通过`loss_weight`指定参数的权重。
>
>`model.compile(optimizer='rmsprop', loss='binary_crossentropy',loss_weights=[1., 0.2])`

##4.其他拟合、训练、测试同Sequential。
##To continued...