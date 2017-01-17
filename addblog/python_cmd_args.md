title=Python优雅地处理命令行参数
en_title=python
category=Python
tags=Python,ArgumentParser
summary=哒溜君最近写python的时候总是会遇到要处理命令行参数的问题，这个东西其实调用sys.argv其实就可以解决了，但是这个玩意有一个致命的弱点就是里面有些参数我要自己一点一点的去分析，而不能很优雅地拿到这些参数的值，繁杂的工作让哒溜君整个人都不好了。。。直到最近哒溜君发现了一个叫做ArgumentParser的模块。
<ep_info>
[转帖请注明出处www.wangqingbaidu.cn](www.wangqingbaidu.cn)

#一、 使用模板
<pre class="brush:python;">
import  argparse
parser = argparse.ArgumentParser(description='balabala')
parser.add_argument(args)
args = parser.parse_args()</pre>

#二、 参数介绍
其中`add_argument`的函数原型是

`ArgumentParser.add_argument(name or flags…[, action][, nargs][, const][, default][, type][, choices][, required][, help][, metavar][, dest])`
>1.`name or flags`
>
>这个参数没有`_`或者`__`的参数列表，也就是相应的位置参数，在命令行运行的时候是不能缺少的。
>
>2.`nargs`
>
>指定的是这个参数后面有几个输入数据，可以是正则表达式，或者数值，如果是`*`则适配所有参数。

其他的参数应该比较好理解了。