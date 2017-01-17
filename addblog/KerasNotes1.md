title=Keras深度学习框架学习笔记
en_title=kerasNotes
category=DeepLearning
tags=DeepLearning,Theano,Keras
summary=此系列笔记为小w在鼓捣PRNN（DeepMind 16 paper）遇到的各种各样的问题，这个给大家分享一下，Keras是基于Theano的深度学习框架。目前此笔记为乱序状态，各位太君按需求自行索取，后续会对笔记进行整理。
<ep_info>

首先来讲一讲Keras的models，这是Keras的入口，也是必须要掌握的，类似于caffe中的prototxt文件，只不过Caffe是通过配置文件的形式，但是Keras通过的是python代码直接配置的。

#一、Common Sense
手写介绍一下Keras中一般一定会遇到的一些基本问题。

###1.Model载入
>这估计是所有人都关心的问题了，也是深度学习为什么这几年这么火的一个重要原因，就是我可以重现别人的实验，当然是有前提的，就是别人要贡献出模型配置代码和训练好的参数。
>>小w最近就比较苦逼，在重现PRNN但是这是DeepMind的论文，没有开源也就算了，论文有些地方写的还让别人各种瞎猜，我也是醉了。

>模型的配置可以通过`yaml`文件进行存储，也可以将其转化成json格式，使用也很简单。

>>     from models import model_from_yaml
	yaml_string = model.to_yaml()
	model = model_from_yaml(yaml_string)

>>     from models import model_from_json
	json_string = model.to_json()
	model = model_from_json(json_string)

>个人推荐使用yaml，好像是Caffe也可以通过加载，所以这样可以实现Caffe Model到Keras Model的转化。

###2.Weights载入
>跟Model一样，它与Model构成了NN的两大要素。Keras有两种载入weights的方法。
>> 1.`set_weights(weights)`

>此方法只能使用在模型运行时调用`get_weights()`进行载入，他返回的是一系列的numpy arrays。 

>> 2.`load_weights(filepath)`

>此方法的参数格式为HDF5格式的，可以使用`save_weights(filepath)`进行参数保存。

>前者主要是在model训练的时候进行参数的保存，后面主要是对参数持久化到磁盘上。但是前者要是想持久化到磁盘上其实也是可以的，使用cpickle对其进行存储，但是Keras的官方文档不推荐这么做。


#二、Sequential
Sequential是串行的网络模型，基本上适合于目前主流的网络结构，包括*AlexNet, VGG-X, GoNet*等等 
###1.初始化
>`model = Sequential()`

>模型初始化之后就可以在后面添加你想要的layer了。

###2.按需添加layer
>接下来的工作就比较简单了，下面给大家举个例子

>>     model.add(Convolution2D(32, 3, 3, border_mode='same',
                        input_shape=(img_channels, img_rows, img_cols)))
	model.add(Activation('relu'))

>这是一个层的网络配置，后面的大家可以添加con1d, lstm, dense... 这里要说明的一点事，在网络的第一层需要制定输入的`input_shape`。因为你不告诉Keras，他是没有办法推测的。但是后面的层就需要了，因为他会自己推断出来，如果看源码就会知道，它有一个`get_output_shape_for`的函数来推断上一层的输出。

###3.Compile整个网络
>这一点可能是比较难理解的，这里给大家做一个简单的解释，因为Keras是搞Theano的那帮人在T上进一步封装搞起来的，虽然后面支持的Tensorflow引擎，但是最native的还是使用Theano引擎。而Theano的设计很有意思，虽然使用python写的，但是感觉更像一门新的语言。只不过语言需要遵守python的语法。

>Theano在未调用`compile`方法之前是不会对立面的任何参数进行赋值，所有的参数在Theano看来都是Tensor(标号)，就想一个图，他只是说明途中有哪些节点，但是节点的值是没有定义的。所以你不能在程序跑的过程中去打印任何的Theano变量。如果各位太君想深入了解，还请去参考[Theano的官方文档](http://deeplearning.net/software/theano/tutorial/index.html#tutorial)，当然后续的文章也会对这个问题进行讨论。

>好回到刚才的问题，`compile`就是对Keras学习框架图的一个构建。

>>`compile(self, optimizer, loss, metrics=[], sample_weight_mode=None)`

>小w基本只关注 `optimizer`, `loss`两个参数，但是如果仅仅是浮现简单的实验，它的定义也十分简单

>>     sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
	model.compile(loss='categorical_crossentropy', optimizer=sgd)

>到此一个最简答的网络就设计完成了。

###4.训练拟合
>训练的过程在简单不过，跟大多数的基于python写的数据挖掘的包（Scikit-learn）是一样的，最常用的就是一个`fit`和`predict`函数。
>
>>     model.fit(X_train, Y_train, batch_size=batch_size,
              nb_epoch=nb_epoch, show_accuracy=True,
              validation_data=(X_test, Y_test), shuffle=True)

>怎么去拿到训练数据这是跟业务相关的，需要各位太君自己去摸索，但是Keras在example中会提供一些预定的数据集加载的函数，感兴趣的童鞋可以去参考`Keras_HOME/datasets/`以及`Keras_HOME/utils/data_utils.py`里面的代码，可以给各位太君一些获取数据的灵感。

>`batch_size`可以设置一下，这个决定更新的频率，也就是在多少个训练数据之后进行参数的更新。不过听师兄说，这个`batch_size`好像对最后模型的好坏影响不大。

###5.模型评估
>一般作用在validation set上，用于评估当前网络的好坏。

>>`evaluate(self, x, y, batch_size=32, verbose=1, sample_weight=None)`

###6.模型测试
>这个过程就是调用`predict`的过程，十分简单，一行代码`predict(self, x, batch_size=32, verbose=0)`搞定，当然如果想知道每一个类别对应的概率，则可以使用`predict_proba(self, x, batch_size=32, verbose=1)`。


#三、Functional API
这个功能着实吓了小w一跳啊，貌似强大到不能在强大了，遥想当年小w还在用Graph的时候(如果原来2016.4之前接触过Keras的话，应该对Graph很熟悉)，就感觉已经屌的不行不行的了。


##To continued...