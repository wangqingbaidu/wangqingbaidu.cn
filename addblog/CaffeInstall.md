title=Ubuntu14.04、Centos安装Caffe以及相关依赖
en_title=caffe
category=DeepLearning
tags=DeepLearning,Linux,Caffe
summary=这篇文章是我们组的大神亲自安装caffe的笔记，如果有问题，可以联系Email:liuhuan@ict.ac.cn
<ep_info>

#Ubuntu14.04、Centos安装Caffe以及相关依赖
这篇文章是我们组的大神亲自安装caffe的笔记，记录相当详细，并且多次参考，亲测可用（我们喜欢动不动重装系统。。。）如果有问题，可以联系Email:liuhuan@ict.ac.cn
####<font color=red>Caffe如果使用GPU请自行安装CUDA，在NVIDIA官网直接下一个.run文件，关闭图形界面就可以直接安装了，很easy，就不再赘述。</font>

#一、Ubuntu14.04
###1.download Caffe from github
>`git clone https://github.com/BVLC/caffe`
>
>following the installation on [http://caffe.berkeleyvision.org/installation.html](http://caffe.berkeleyvision.org/installation.html)
>
###2.install OpenBLAS 
>`git clone https://github.com/xianyi/OpenBLAS/`
>
>`sudo make && sudo make install`
>
###3.install protobuf
> `git clone https://github.com/google/protobuf`
>
>`./autogen`
>
>`./configure`
>
>`sudo make && sudo make install`
>
###4.install gmock and rename
>[https://github.com/paulsapps/gmock-1.7.0](https://github.com/paulsapps/gmock-1.7.0)
>
>`mv gmock-1.7.0 ../protobuf/gmock`
>
###5.update  autoconf
>`sudo apt-get install autoconf`
>
>`sudo ldconfig`
>
>`cd caffe`
> 
>`./autogen`
>
>更改Makefile.conf的`INCLUDE_DIR`添加 hdf5的头文件路径我的机器上安装的hdf5之后的路径为：`/usr/include/hdf5/`<font color=red>serial/</font>并添加`hdf5.so `的路径然后`sudo ldconfig`

###Tips:
>1. 遇到问题再查吧，如果遇到没有安装的软件或者依赖使用`apt-cache search software`这样一步一步就能够安装软件了。
>
>2. 查看显卡：`lspci`；
>显卡的型号：`lspci | grep VGA`；
>查看nvidia显卡：`lspci | grep -i nvidia`；

#二、Centos6.5:
###1.安装snappy-devel，opencv-devel，boost-devel，protobuf,
>`yum install protobuf-devel leveldb-devel snappy-devel opencv-devel boost-devel hdf5-devel`
>
>成功安装的：eveldb,glog,gflags,lmdb,atlas-devel,opencv-devel,boost-devel,snappy-devel

>####centos6.5 install protobuf
>>`sudo wget http://protobuf.googlecode.com/files/protobuf-2.5.0.tar.bz2`
>
>>`tar -xf protbuf.tar.bz2`
>
>>`cd protobuf`
>
>>`make -j && make install`
>
>>查看挂载列表：
>
>`blkid -c /dev/null -o list`

###2. opencv2.4.13
>`cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D BUILD_PYTHON_SUPPORT=ON -D BUILD_EXAMPLES=ON ..`
>
>`make && make install`

#三、Centos7
>###centos7 install caffe:
>`sudo yum install protobuf-devel  snappy-devel  boost-devel` 
>###1.安装 glog
>>`wget https://google-glog.googlecode.com/files/glog-0.3.3.tar.gz`
>
>>`tar zxvf glog-0.3.3.tar.gz`
>
>>`cd glog-0.3.3`
>
>>`./configure`
>
>>`make && make install`
>
>###2.安装 gflags
>>`wget https://github.com/schuhschuh/gflags/archive/master.zip`
>
>>`unzip master.zip`
>
>>`cd gflags-master`
>
>>`mkdir build && cd build`
>
>>`export CXXFLAGS="-fPIC" && cmake .. && make VERBOSE=1`
>
>>`make && make install`
>
>###3.安装 lmdb
>>`git clone https://github.com/LMDB/lmdb`
>
>>`cd lmdb/libraries/liblmdb`
>
>>`make && make install`
>
>>`sudo yum install atlas-devel`
>
>>`git clone https://github.com/gflags/gflags.git`
>
>>cmake2.8.12 以上
>
>>`tar -zxf cmake*.tar.gz`
>
>>`cd cmake && make -j && make install`
>
>>才能编译gflags
>
>>`git clone https://github.com/google/leveldb`
>
>>复制动态库到`/usr/local/lib`
>
>>头文件到`/usr/local/include`
>

#四、CentOS 7 CUDA安装
安装文件为.run文件，安装比较方便。本身包含了驱动程序。

下载地址：[https://developer.nvidia.com/cuda-downloads](https://developer.nvidia.com/cuda-downloads)

安装文档参考：[http://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#runfile](http://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#runfile)

1.创建一下文件 `/etc/modprobe.d/blacklist-nouveau.conf` ，写入一下内容
>
     blacklist nouveau
     options nouveau modeset=0

2.重新生成 kernel initramfs:` sudo dracut --force`

3.关闭XServer，shell中运行` init 3`  进入文本模式

#五、其他依赖
>###A.源码安装Boost
>1.下载源代码[https://github.com/boostorg/boost](https://github.com/boostorg/boost) 或者[https://sourceforge.net/projects/boost/files/boost/1.61.0/boost_1_61_0.tar.bz2](https://sourceforge.net/projects/boost/files/boost/1.61.0/boost_1_61_0.tar.bz2)
>
>2.`./booststrap`
>
>3.`./b2 install` 为默认安装路径`/usr/local`
也可以使用 --prefix=path_to_install来指定安装路径。

>###B.源码安装Cmake3.5.2
>1.解压源码
>
>2.`./bootstrap`
>
>3.`gmake`
>
>4.`gmake install`

>###C.源码安装gflags
>1.下载源代码[https://github.com/gflags/gflags](https://github.com/gflags/gflags)
>
>2.解压文件
>
>3.`mkdir build && cd build`
>
>4.ccmake .. 这一步来选择生成动态库
>
>5.`make -j && make install`

>###Tips:
>>没有安装CUDA可以使用下面这条命令
>>`cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local/opencv ..`
>
>>安装了CUDA使用下面这条命令可以解决出现的问题
>>`cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local/opencv -D CUDA_GENERATION=Kepler INSTALL_PYTHON=ON ..`
>
>>`make -j && make install`

#六、可能遇到问题：

####1. install hdf5下载已经编译好的hdf5.1-8.tar.gz文件然后把动态库复制到`/usr/local/lib` 下面，把头文件复制到`/usr/local/include`下面

####2. leveldb下载编译好的leveldb把include/leveldb 复制到/usr/local/inlucde当中就可以

####3. lmdb 
>`git clone https://github.com/LMDB/lmdb`
>
>` cd lmdb/libraries/liblmdb`
>
>` make && make install`

####4. 遇到的问题：
undefined reference to `cblas_sgemv'。。。这个是在Makefile.config当中BLAS:=open 后面多了一个空格。所以在这一行需要以open结尾，后面不能有空格 WTF!。
