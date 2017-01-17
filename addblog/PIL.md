title=使用PIL，自动生成图片（验证码）
en_title=pil_pic
category=Environment
tags=linux,python,PIL
summary=在linux上使用PIL（python处理图片的库）生成图片。但是会遇到很多坑，网上的解决方案没有一个全的，可能还是大家的环境不一样。接下来小w就给大家做一个总结。因为我是从纯净版的centos6.5开始安装的，自信可以cover各位所有的坑。
<ep_info>

#Linux中使用PIL生成验证码
因为最近在用django写网页，就想到写一个生成验证码的程序，因为django是用python的，所以很自然的就想到了用PIL，网上一Google就发现，哇果然好多源码，很高兴下载了一个，以为可以很快搞定，但是理想很丰满，现实却很骨感。Too young too naive!

##naive实现
大家很容易就想到了怎么搞了，copy网上源码，由于要使用到PIL，所以pip一下就行了，以为2步可以搞定，嗯！

>1. `pip install PIL`
>2. `python src.py`

以为这样就搞定的，那你真是想多了。。。
首先第一步就行不通
执行上面命令，你就会发现
<font color='red'>Could not find any downloads that satisfy the requirement PIL</font>
哈哈恭喜你，还是老老实实从源码安装吧。

##PIL安装
>1. `pip uninstall PIL`
>2. `pip uninstall pillow`
>3. `wget http://effbot.org/downloads/Imaging-1.1.7.tar.gz`
>4. `tar -zxf Imaging-1.1.7.tar.gz`

好到此为止源码下载完成，先别记着安装，因为需要装依赖，分别是`jpeglib`和`freetype-devel`

* 先安装`freetype-devel`(因为比较好安装, 你的环境可能已经有)，使用`yum install freetype-devel`
* 接下来安装jpeg库

	>1. `wget http://www.ijg.org/files/jpegsrc.v7.tar.gz`
	>2. `tar -zxvf jpegsrc.v7.tar.gz`
	>3. `cd jpeg-7`
	>4. `CC="gcc -arch x86_64"`
	>5. `./configure --enable-shared --enable-static`
	>6. `make`
	>7. `make install`

ok，目前在生成验证码的路上你已经走了一般的路。

* 修改Imaging-1.1.7目录下的setup.py文件找到JPEG_ROOT 和 FREETYPE_ROOT
		
		JPEG_ROOT = libinclude("/usr/local")
		FREETYPE_ROOT = '/usr/lib64','/usr/include/freetype2/freetype'

* 将`/usr/local/lib`加入到你的动态链接库
	>1. `echo 'usr/local/lib' >> /etc/ld.so.conf`
	>2. `ldconfig`
	
* 最后在Imaging-1.4.7文件中使用`python setup.py build_ext -i`查看支持项（在最末尾），注意留意`--- FREETYPE2 support available`有没有支持。然后进行最畅快人心的`python setup.py install` 

ok，恭喜你，此时你的PIL库算是安装成功了！！！

##python src.py
下面给大家附上生成验证码的源码地址，拷贝自[CSDN](http://blog.csdn.net/cdnight/article/details/49636893)

python一下你就会发现<font color='red'>`IOError: cannot open resource`</font> 定位位置发现是里`font = ImageFont.truetype(font_type, font_size)`哦哦，看一下font_type='arial.tty' 使用`fc-list`看一下安装的字体，发现原来是字体没有安装，那好吧安装字体。

##linux 字体安装
在这里就不再赘述字体怎么从Windows导入到linux，网上教程一大堆，不过还是个大家一个[连接http://www.cnblogs.com/sqmlinux/archive/2012/08/20/2646993.html](http://www.cnblogs.com/sqmlinux/archive/2012/08/20/2646993.html)

好的，我假设你的字体安装搞定了，使用`fc-list`可以查到你想要的字体了。

##大功告成
好了终于可以继续python一下了。
发现还是原来的错误，what? 白搞了？

没有，从Windows弄下来的字体是大写的，并且需要制定路径，最后修改一下源码的`font_type='/usr/share/fonts/win_arial/ARIAL.TTF`就好了。注意`/usr/share/fonts/win_arial`请改成你字体存放路径。

##show一下
![验证码](http://i.imgur.com/BdqNGh7.jpg)