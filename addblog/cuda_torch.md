title=向torch中添加cuda自定义layer
en_title=dltb
category=DLToolBox
tags=DeepLearning,Torch,Cuda,CustomLayer
summary=哒溜君总是这样觉得，深度学习是十分easy的，因为你可以随便拿过一个深度学习的框架，用10行左右的代码构建出一个不会很差的模型。但是话虽是这么说，但是这些也就只能提供一个baseline，也就是100公里的路，虽然任务已经完成了90%，但是最艰难的就是剩下10%。而且哒溜君觉得深度学习的精髓在于自定义的layer（当然那些研究网络模型例如vgg，resnet的也很叼）。本文就是用一个例子给大家介绍如何在torch上添加自定义的layer并且让他跑在GPU上。
<ep_info>

[转帖请注明出处www.wangqingbaidu.cn](www.wangqingbaidu.cn)
#丰富torch——向torch添加自定义layer（运行在GPU）
如何在torch里面添加自定义的layer哒溜君感觉已经不需要我在这里赘述了，相信大家至少已经阅读了torch的官方文档或者其他的一些博客，如果各位大侠这都没来的及看的话，下面给大家提供一下连接。

>官方文档:[http://torch.ch/docs/developer-docs.html](http://torch.ch/docs/developer-docs.html)

>很不错的一个博客: [https://zhuanlan.zhihu.com/p/21550685](https://zhuanlan.zhihu.com/p/21550685)

这篇博文不打算详细到将各种torch里面的运行机制balabala，话说我本人也不是很清楚~~

当然也不会涉及很高深的cuda，话说我本人也不会~~~

这篇文章主要是结合哒溜君做的工作，用一个例子，告诉大家如何照着torch里cunn的源码，照葫芦画瓢地写出一个可以跑在cuda上面的layer。他不是详解，更像是一个方向，如果各位大侠想做更深入的了解可以参考文章中各处给出的连接。如有不对的地方，还望雅正。

##一、自定义中3个必须实现的函数的理解
在torch中实现自定义layer时不需要实现3个核心的函数，分别是`updateOutput(input)`,  `updateGradInput(input, gradOutput)`, `accGradParameters(input, gradOutput)`

下面对这三个函数的作用做详细的介绍。

###1.`updateOutput(input)`函数
顾名思义，这个函数主要是用在前馈网络中，用来计算当前层的一个输出

>在module（其实我更喜欢叫他model）的forward中会被调用。 当前层的逻辑就是 
>
>$$Y = F(X)$$
>
>其中X是上一层的输入，Y是输出，F为updateOutput

###2.`updateGradInput(input, gradOutput)`函数
这个函数是在bp的时候调用，通过上一层传过来的loss（好多人喜欢说成loss，其实哒溜君感觉这里不能称之为loss，因为在bp的时候，最后一层的loss function的输出产生的那个结果其实是不参与bp的，而我们习惯性称之为loss，但是真正参与bp的是loss function求导之后作用输入产生的那个结果参与bp）也就是`gradOutput`计算当前层要传递给上一层的输入。

>bp的过程相当于就是一个不断使用链式法则求导的过程。对于函数
>
>$$f(x) = h(g(x))$$
>
>f对x的导数为
>
>$$f'(x) = \frac{\partial h(x)}{\partial g(x)} \times  \frac{\partial g(x)}{\partial x} $$
>
>上文说的`Y = F(X)`其实并不是很确切或者说只是对前向传播时确切的。因为正常来说每一层的输出函数为`Y = F(X, w)`，其中`w`也就是网络的参数，例如卷积层中filer里面的参数。但是输入`X`和参数`w`是相互独立的，所以在对求梯度的时候可以固定一个求另一个。
>
>在求要传递给上一层的梯度`updateGradInput`时固定`w`，也就是对于输入的梯度还是关于X的方程，在bp的过程中需要求出输出对于输入的偏导，也就是
>
>$$\frac{\partial E}{\partial X} = \frac{\partial E}{\partial Y} \times  \frac{\partial Y}{\partial X} \quad gradOutput = \frac{\partial E}{\partial Y}$$
>
>E依然是最终定义的loss function

###3.`accGradParameters(input, gradOutput)`函数
这个函数是用来更新网络里面的 `weights` 以及 `bias`，其理解与GradInput相同，只不是现在是固定`X`对`w`求偏导，这一层是可选的更新层，因为有些层中是不存在参数的，像`Dropout`以及各种`Pooling`层。

理解同上就不再赘述。

###4.总结
到目前为止为啥一定要实现这三个（如果对应层没有参数就是两个）函数有了一定的了解，如果这个地方不能理解，估计自己写出来的layer要不不能跑，要么就会出现bug。

##二、一个具体的例子----GlobalAveragePooling
ok，读到这里我默认大家已经对如何添加自定义的layer比较熟悉，如果仍然一头雾水，请继续阅读前文提供的官方文档连接已经那个和不错的blog。

下面就直接进入例子，GlobalAveragePooling

###1.GlobalAveragePooling用途
先介绍一下这个layer到底是干什么的，要不然会很费解。这个layer其实是类似于`AveragePooling`, 但是`AveragePooling`在使用的时候需要制定pooling的核的大小，并不能达到一个整张feature map pooling的效果，你可能会说我可以把pooling核定义成输入的feature map的大小，当然这个方法可以，但是有一个前提就是你必须知道输入的feature map是多少，这时你又会说，这很容易啊，算一下不就行了，确实算一下就行了，但这时候又有一个前提就是对于你的每一个图片它输入的feature map都是固定大小的，这时你又会说，是固定大小的啊，这时我只能说你肯定没有跟进最新的CNN网络。首先说为什么feature map是固定的，就是因为全连接层的限制，因为它要求输入的节点个数固定，这时一般在输入网络时会对图像做resize。但是随着FCN的流行，全连接层逐渐被抛弃，输入到网络的图像可以是任意尺度，这时候如果使用固定`AveragePooling` 核的大小就不能起到相应的效果了。

><font color=red>ok，上面全是扯淡~~</font>
>
>一言以蔽之，将输入Averagepooling成一个值（任意尺度）。

>表现在tensor上的效果就是：batch_size * filter * w * h ----->  batch_size * filter * 1 * 1

###2. Cuda实现
CPU版本的就不说了，算法是比较简单的，大家可以自行实现，如论你是直接在lua里面实现，还是用c实现。下面就介绍哒溜君咋写Cuda代码的时候遇到的坑。

>首先肯定是参考人家（`AveragePooling`）的源代码怎么写，照葫芦画瓢吗~~
><pre class='brush:cpp'>THCUNN_assertSameGPU(state, 2, input, output);
 THArgCheck(input->nDimension == 3 || input->nDimension == 4, 2, "3D or 4D (batch) tensor expected");
  long nInputCols, nInputRows, nInputPlane, batchSize;
  long nOutputCols, nOutputRows;
  if (input->nDimension == 3) {
    nInputCols = input->size[2];
    nInputRows = input->size[1];
    nInputPlane = input->size[0];
    batchSize = 1;
  }
  else
  {
    nInputCols = input->size[3];
    nInputRows = input->size[2];
    nInputPlane = input->size[1];
    batchSize = input->size[0];
  }</pre>

>可以看到这些都是功能性的，仔细看了一下索性不再修改了~~，再继续往下看
><pre class='brush:cpp'>if(ceil_mode) {
    nOutputCols = ceil(float(nInputCols - kW + 2*padW) / float(dW)) + 1;
    nOutputRows = ceil(float(nInputRows - kH + 2*padH) / float(dH)) + 1;
  }
  else {
    nOutputCols = floor(float(nInputCols - kW + 2*padW) / float(dW)) + 1;
    nOutputRows = floor(float(nInputRows - kH + 2*padH) / float(dH)) + 1;
  }
  if (padW || padH)
  {
    // ensure that the last pooling starts inside the image
    // needed to avoid problems in ceil mode
    if ((nOutputRows - 1)*dH >= nInputRows + padH)
      --nOutputRows;
    if ((nOutputCols  - 1)*dW >= nInputCols  + padW)
      --nOutputCols;
  }</pre>

>这些是用来通过给定的输入w，h计算输出的，因为我们这个是Global的池化，所以无论你输入什么，我只输出一个值，所以也就是不要他们了，各位大侠在自己实现的时候可一定要注意，并不意味着各位也不需要计算输出的尺寸。
>
><pre class='brush:cpp'>input = THCudaTensor_newContiguous(state, input);
  float* input_data = THCudaTensor_data(state, input);
  THCudaTensor_resize4d(state, output, batchSize, nInputPlane, nOutputRows, nOutputCols);
  float* output_data = THCudaTensor_data(state, output);
  int count = THCudaTensor_nElement(state, output);
</pre>

>这个里面首先要将输入弄到一片连续的空间（输入不一定是连续的空间，大家可以参考torch里面tensor的select等片选函数），这一定至关重要，因为后面都是使用类似c的联系内存进行index索引的。
>接下来是resize，其实不用太care，只是吧output的数据结构确定下来，就下来就是申请刚才的那么大的存在显存的数据结构了。
>最后计算要输出的元素的个数，这个值决定着要申请的GPU的流处理器的个数。在本例中申请的是batch_size * filter * 1 * 1个，也就是要有这么多的流处理器进行并行运算。

><pre class='brush:cpp'>AvePoolForward<float, true><<< GET_BLOCKS(count), CUDA_NUM_THREADS, 0, THCState_getCurrentStream(state) >>>
(count, input_data, batchSize, nInputPlane, nInputRows, nInputCols, nOutputRows, nOutputCols, kH, kW, dH, dW, padH, padW, output_data);</pre>

>`GET_BLOCKS(count)`这个函数就是计算要运算的并行度，`CUDA_NUM_THREADS`宏定义，torch源码设置为1024，剩下的就是里面的一堆参数，balabala~~~，接下来看看这个函数怎么具体实现的。
>
>在cuda中要在GPU中执行的函数以`__global__`标示
><pre class='brush:cpp'>template < typename Dtype, bool COUNT_INCLUDE_PAD >
__global__ void AvePoolForward(const int nthreads,
    const Dtype* const bottom_data, const int num, const int channels,
    const int height, const int width, const int pooled_height,
    const int pooled_width, const int kernel_h, const int kernel_w,
    const int stride_h, const int stride_w, const int pad_h, const int pad_w,
    Dtype* const top_data) {
         CUDA_KERNEL_LOOP(index, nthreads) { balabala~~~}
    balabala~~~}</pre>

>看看源码可以看见，这个函数其实就是执行的一个`CUDA_KERNEL_LOOP`函数，然后它是两个参数`index`和`nthreads`第二个参数传进来的就有啊，但是index这个参数在什么地方，找遍了这个文件都没有，<font color=red>what's the fuck?</font> 这个地方困扰哒溜君良久，简直日狗，最后看源码发现，原来`TMD`的这是宏定义，下面来看一下这个宏定义是什么。。。
><pre class='brush:cpp'>#define CUDA_KERNEL_LOOP(i, n) \
  for (int i = blockIdx.x * blockDim.x + threadIdx.x; i < (n); i += blockDim.x * gridDim.x)</pre>

>原来index是在这里面呗传进来定义的。
>
>具体cuda的执行原理请参见[http://blog.csdn.net/augusdi/article/details/12833235](http://blog.csdn.net/augusdi/article/details/12833235)
>
>这里仅简单介绍一下整个代码的执行逻辑，首先在没有进入`__global__`函数之前，代码是在cpu上执行的，也就是串行执行，当调用这个函数之后，切换到GPU执行，这时候执行就是一个并行执行的了，但是这时候各位大侠就要问了，既然是并行执行为啥还要`for`循环去执行呢？这个问题很好，因为当初也困扰了我很长的时间，哎~~，到底为什么呢？
>
>其实在现在的体系结构中在单个处理单元中并没有真正的并行，都是串行的，大家去看for循环的步长，`blockDim.x * gridDim.x`这个值是多少，其实就是我们刚才使用`GET_BLOCKS(count)`函数申请的处理单元的个数，也就是有这么多的处理单元在并行处理，但是如果我们的n，也就是输出大于我们申请的处理单元的个数之后，那么它还是会串行的执行下一个步长的数据。
>
>因为哒溜君的全局pooling不用考虑filer的kernel的，所以不存在位置的问题，但是这里提醒各位大侠，并不意味着大家也不用去考虑，对于指定的位置的数据，大家还要使用`blockDim.x`, `gridDim.x`, `index`去获取，这个就不一而足了，要各位大侠具体问题具体分析。

####3.总结
到此为止基本上把怎么编写cuda的自定义layer讲的差不多了，剩下的就是参考前文提到的博客把指定的文件copy到指定的目录，然后在修改执行的文件内容，从新编译就好了，就不再赘述。

##三、One more thing, 关于自定义cuda layer的一点不成熟的小想法
编写自定义的layer在实际工业生产中很重要，相信各位大侠深有体会，但是是不是遇到torch没有的layer我们就去自己写cuda代码吗?哒溜君必以为然（科普一下，它的意思是不认为是对的）。

其实在很多的时候，我们可以通过torch自带的数学运算实现，因为torch本身自带的tensor是支持CPU，GPU运算的，如果一个layer可以通过torch自带的一些数学运算得出，就没有必要去写这个cuda代码（毕竟比较蛋疼）。。。

还是举哒溜君自己实现的`GlobalAveragePooling`的例子，在前馈网络中，其实我们只要对4d tensor的最后两维的数据求一个均值就好了，非要搞的这么麻烦做什么，`torch.mean(torch.mean(x, 4),3)`这条简单的命令就实现了cuda代码的功能，岂不是很easy，而且自己写还会有各种潜在的bug（并不是哒溜君不自信。。。）

下面看看torch里面到底提供了那些数学运算

[http://torch7.readthedocs.io/en/rtd/maths/](http://torch7.readthedocs.io/en/rtd/maths/)

ok哒溜君只能帮你倒这里了，下面share一下自己的`SpatialGlobalAveragePooling`的github代码，使用中切<font color=red>记</font>使用 `:cuda()`进行GPU运算，要不然跑不了（哒溜君比较懒，没有实现CPU的版本，如果没有会出现`SpatialGlobalAveragePooling in CPU is not implemented!`错误）

☛[github代码]()☚