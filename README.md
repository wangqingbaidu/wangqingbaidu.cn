# [http://www.wangqingbaidu.cn/](http://www.wangqingbaidu.cn/)
我个人博客的源码，安装文档大家请参考[http://www.wangqingbaidu.cn/article/untitled1460536273.html](http://www.wangqingbaidu.cn/article/untitled1460536273.html)

##我自己添加的功能

1.自动添加markdown形式的博客。但是必须按照指定格式编写。下面的是一个示例。这些都是博客的元信息。最好不要为空。

>```
title=Papers on Deep Learning(Deep Embedding with Contextual Evidences)
en_title=dlp
category=Papers
tags=DeepLearning,Papers,ImageRetrival
summary=eee
<ep_info>
```

2.代码块支持，在markdown代码中添加`<pre class="brush:cpp;">code view </pre>` 其中`cpp`可以修改为`python`, `powershell`, `xml`, `java`, `jscript`

3.ppt功能（阉割版，只能展示图片），url在/show_ppt/XXXX里面， 例子[http://www.wangqingbaidu.cn/show_ppt/XNORNET](http://www.wangqingbaidu.cn/show_ppt/XNORNET), 文件的存放路径`~/myblog/blog/blog/static/pptx`

4.LaTex代码支持，`$$a=\sum_{n=1}^N{n}$$` 


##说明
1.addblog文件夹中为哒溜君博客添加的所有博客内容，大家可以参考里面博客的形式。

2.blog为vmaig博客的拷贝，但是增加上面的功能。


___

    python manage.py migrate
    python manage.py createsuperuser
    
运行 :
    
    python manage.py runserver
    
    
# 生产环境部署
	
使用docker部署，首先pull下来image或者自己使用项目中Dockerfile或者Dockerfile_cn build。
	
	sudo docker pull billvsme/vmaig_blog
然后运行image  
	例子:
	
	sudo docker run -d -p 80:80 --name vmaig\
                            -e WEBSITE_TITLE='Vmaig'\
                            -e WEBSITE_WELCOME='欢迎来到vmaig'\
                            -e EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend' \
                            -e EMAIL_HOST='smtp.163.com'\
                            -e EMAIL_PORT='25'\
                            -e EMAIL_HOST_USER='yourname@163.com'\
                            -e EMAIL_SUBJECT_PREFIX='vmaig'\
                            -e EMAIL_HOST_PASSWORD='yourpassword'\
                            -e QINIU_ACCESS_KEY='your_as_key'\
                            -e QINIU_SECRET_KEY='your_sr_key'\
                            -e QINIU_URL='your_url'\
                            -e QINIU_BUCKET_NAME='your_bucket_name'\
                            billvsme/vmaig_blog
    
**环境变量**:  
其中：EMAIL_HOST，EMAIL_PORT，EMAIL_HOST_USER，EMAIL_HOST_PASSWORD是必须的，如果不指定，用户注册不了

	WEBSITE_TITLE  网站的title
	WEBSITE_WELCOME  首页显示的欢迎消息
	
	EMAIL_BACKEND  email的引擎，默认是django.core.mail.backends.smtp.EmailBackend，如果想支持qq邮箱请使用django_smtp_ssl.SSLEmailBackend
	EMAIL_HOST  SMTP地址
	EMAIL_PORT  SMTP端口
	EMAIL_HOST_USER  邮箱名称
	EMAIL_HOST_PASSWORD  邮箱密码
	EMAIL_SUBJECT_PREFIX  邮件Subject-line前缀
	
	# 默认头像保存在服务器，如果想保存在七牛中要定义下面这些环境变量
	QINIU_ACCESS_KEY  七牛的access key
	QINIU_SECRET_KEY  七牛的secret key
	QINIU_BUCKET_NAME  七牛的bucket
	QINIU_URL  七牛的url
	
运行后，默认管理员用户名为 admin，密码为 password ， 请登录 http://your-domain/admin 更改密码。                   

#接下来该干什么？
在浏览器中输入 http://127.0.0.1:8000/admin  
输入前面初始化数据库时的用户名密码。  
后台中，可以  
通过“轮播”添加首页的轮播  
通过“导航条”添加首页nav中的项目  
通过“专栏” 添加博客专栏（可以和导航条结合起来）  
通过“资讯” 添加转载的新闻  
通过“分类” “文章” 添加分类跟文章  
通过“用户” 对用户进行操作  

**特别注意**
首页的便签云中的内容，在后台不能修改。
请修改  blog/templates/blog/widgets/tags_cloud.html 中的 tags数组的内容。
