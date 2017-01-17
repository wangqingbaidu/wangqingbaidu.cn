# [http://www.wangqingbaidu.cn/](http://www.wangqingbaidu.cn/)
我个人博客的源码，安装文档大家请参考[http://www.wangqingbaidu.cn/article/untitled1460536273.html](http://www.wangqingbaidu.cn/article/untitled1460536273.html)

我自己添加的功能

1. 自动添加markdown形式的博客。但是必须按照指定格式编写。下面的是一个示例。这些都是博客的元信息。最好不要为空。

>```
title=Papers on Deep Learning(Deep Embedding with Contextual Evidences)
en_title=dlp
category=Papers
tags=DeepLearning,Papers,ImageRetrival
summary=eee
<ep_info>
```

2. 代码块支持，在markdown代码中添加`<pre class="brush:cpp;">code view </pre>` 其中`cpp`可以修改为`python`, `powershell`, `xml`, `java`, `jscript`

3. ppt功能（阉割版，只能展示图片），url在/show_ppt/XXXX里面， 例子[http://www.wangqingbaidu.cn/show_ppt/XNORNET](http://www.wangqingbaidu.cn/show_ppt/XNORNET), 文件的存放路径`~/myblog/blog/blog/static/pptx`
