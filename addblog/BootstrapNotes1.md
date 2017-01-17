title=Bootstrap学习笔记系列（一	）
en_title=Bootstrap
category=Web Design
tags=Bootstrap,Web
summary=简单介绍一下Bootstrap的引用，以及对移动设备的支持。
<ep_info>

使用Bootstrap的好处我就不多介绍了，相信大家对应该有所了解， 我个人感觉他的UI设计还是很人性化的，用起来确实很舒服。

#0. 使用Bootstrap
Bootstrap使用免费的CDN进行加速，所以推荐使用（你可能要问为什么我不自己down放在服务器，其实未尝不可，但是访问你的页面的用户可能也访问了别的基于Bootstrap的页面，而这些js或者css会在dns服务器缓存，这是就会减少别的用户的访问时间）。
>
	<!-- 新 Bootstrap 核心 CSS 文件 -->
	<link rel="stylesheet" href="//cdn.bootcss.com/bootstrap/3.3.5/css/bootstrap.min.css">
>	
	<!-- 可选的Bootstrap主题文件（一般不用引入） -->
	<link rel="stylesheet" href="//cdn.bootcss.com/bootstrap/3.3.5/css/bootstrap-theme.min.css">
>	
	<!-- jQuery文件。务必在bootstrap.min.js 之前引入 -->
	<script src="//cdn.bootcss.com/jquery/1.11.3/jquery.min.js"></script>
>
	<!-- 最新的 Bootstrap 核心 JavaScript 文件 -->
	<script src="//cdn.bootcss.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>

其它的一些支持或者注意什么的可以参考[Bootstrap中文网](http://www.bootcss.com/)

#1.概览
Bootstrap(后面简称B)，专门针对移动设备进行了设计，这个理念是很好的，小w感觉今后的发展方向就是浏览器即应用，使用H5写的页面某些时候跟本地的应用几乎看不出任何差别，大家如果用某宝就会看到有什么某猫的入口，这个入口其实就是H5的页面，是不是感觉跟本地应用很像，是的，B也是这么想的。

在B中，用户所看到的被抽象成一个叫做`viewport`的东西，也得`<meta>`标签需要添加到`<head>`中，如果你要是想在移动设备上用出本地应用的既视感，那就zooming功能禁掉就行。
>`<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">`

另一个要着重说的就是B中的两个容器`container`（固定长宽的）和`container-fluid`（width=100%）

##To continued...