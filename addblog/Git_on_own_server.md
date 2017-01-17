title=构建自己的git服务器
en_title=using_my_own_git
category=Git
tags=git,ssh
summary=本文主要介绍使用git，在自己的服务器上构建代码仓库。小w结合自己的构建代码仓库的时候遇到的坑，分享给各位，希望可以帮助大家快速构架自己的代码仓库。
<ep_info>
#Git on own server
就不蛋疼的介绍什么是git，git和svn或者cvs直接的区别，这些东西小w默认各位太君都已经很了解了，要不然也不会来这里。那么好下面直接进入正题。
##1. Git初始化
	git init 【newrepo】

括号里面的参数是可选参数，如果没有就是在当前目录下创建一个git目录（在linux中是看不见的目录名是.git,如果你非要看，那就使用`ls -a`进行查看），如果有参数就是在指定的目录下创建一个git仓库。

如果成功就会出现

	Initialized empty Git repository in balabala/.git/

如果看不见，估计是各位太君的git没有安装好，还请各位继续完善安装git。

当然在初始化仓库之后还要对仓库的元信息进行初始化，这一点很重要，小w就在这里被坑了。

	$ git config --global user.name "wangqingbaidu"
	$ git config --global user.email wangqingbaidu@wangqingbaidu.cn

name和email使用自己的就行了。

一般情况下我们不会从头开始创建一个新的代码仓库，肯定是已有的代码，想要把他弄到git上去，所以我们应该如何添加我们已有的代码到代码仓库呢？

命令其实so easy！把你已有的代码复制到git仓库目录下，同时在此目录使用

	git add *

一条命令就可以添加你已有的代码了！怎么样是不是so easy！当然你如果不像小w这么懒的话，可以把*替换成你想要添加的文件就行。

最后别忘了确认一下

	git commit -m 'init git'

`-m`后面的东西你可以自己修改，这无关紧要。

##2. 克隆git仓库到本地
上面讲的都是在服务端进行git的初始化,下面介绍在本地使用git的几个常用命令。

>     git clone sshlike_url
sshlike\_url替换成server端代码仓库的位置，例如小w的代码仓库仍在`192.168.1.111`机器的`/home/wangqingbaidu/av`目录下, 那么sshlike_url就要替换成` wangqingbaidu@192.168.1.111:/home/wangqingbaidu/av`

>注意这里的目录后面没有`.git`，这一点要与github进行区分

##3. 配置ssh无密码访问git server
这个为windows里面。使用git bash总是让你输入password for XXX 让人着实蛋疼，小w最最受不了蛋疼的，所以还是配置一下无密码登陆。本以为配置ssh无密码登陆跟linux一样2条命令搞定，看来小w又Too young too naive!

在git bash里面输入ssh-keygen还真有这条命令，那好那我们就开始keygen吧

	ssh-keygen -t rsa
一溜的回车下去就ok了。

当小w继续进行第二条命令是，发现MD，竟然没有`ssh-copy-id`这条命令，这可如何是好 啊！

最后Google发现，其实这条命令指定的操作很简单，就是把pubkey 复制到remote server，所以那小w就手动复制吧
那个公钥的位置在

	C:\Users\wangqingbaidu\.ssh\id_rsa.pub

各位太君请自行在机器中查找,如果你安装了office，请不要用publish软件打开（因为也打不开，哈哈），使用任何记事本打开即可，复制里面全部信息。

在git server的`~/.ssh//authorized_keys`把你复制的内容copy保存过来，就可以在bash中随心所欲的ssh了。

##4. One more thing
本文没有介绍git的基本操作，当然介绍了就跟本文主要要解决的问题不搭嘎了，但是如果各位太君想要了解git的基本操作，可以参考一下下面的连接

[http://www.runoob.com/git/git-tutorial.html](http://www.runoob.com/git/git-tutorial.html)