title=使用jQuery进行异步url请求，获取json格式的数据
en_title=jQuery_ajax
category=Web Design
tags=Web,jQuery,ajax
summary=在js本身提供的ajax调用中，无法解决跨域请求的问题，但是使用jQuery对请求进行封装之后，可以进行跨域请求。
<ep_info>
#jQuery & ajax完成跨域请求json数据

小w目前在玩一个只能家居的项目，但是需要从网络上获取天气数据，怎么办呢？当然可以使用爬虫从网页上爬数据，但是这样繁琐了，应了那句老话，杀鸡焉用牛刀。网上百度了一下(没用Google，感觉这都找不到baidu就太TM low了)。果然找到了一个很神奇的API集市，百度[API Store](http://apistore.baidu.com/)

好多神奇的api，各位小伙伴，如果有需要的可以自行get。
![](http://i.imgur.com/LAUlEV1.png)

那好找到了api就好说了，我们就可以直接用了，什么注册balabala...就不再赘述了。

满心欢喜的以为可以直接用了，发现简直日狗了，根本没有js的调用代码，我去，什么鬼！！！
![](http://i.imgur.com/oQgymb0.png)
好吧，那就自己找呗，发现ajax可以异步进行调用，那好我决定是你了--ajax。

下面来个ajax的标准代码：

	function  get_home_state()
	{
	    var xmlhttp;
	    if (window.XMLHttpRequest)
	    {// code for IE7+, Firefox, Chrome, Opera, Safari
	        xmlhttp=new XMLHttpRequest();
	    }
	    else
	    {// code for IE6, IE5
	        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
	    }
	
	    var api_url = 'www.baidu.com'
	    xmlhttp.open("GET", api_url, true);
	    xmlhttp.send();
	    xmlhttp.onreadystatechange=function()
	    {
	        if (xmlhttp.readyState == 4 && xmlhttp.status == 200 && xmlhttp.responseText != null) { 
	            window.location.assign("http://www.w3school.com.cn")
	        }
	    }
	}

发现根本访问不了，原来原生的ajax不能进行异域访问，我去，好吧！

然后继续找，最好发现了jQuery里面的ajax可以搞定，就决定使用jQuery的ajax。最后终于搞定！

    $(document).ready(function() {
        $.ajax({
            url: 'http://apis.baidu.com/apistore/weatherservice/recentweathers?cityname=%E5%8C%97%E4%BA%AC&cityid=101010100',  
            type: 'GET',                               
            beforeSend: function(request) {
                request.setRequestHeader("apikey", "yourkey");
            },
            success: function (result) {                  
                $("#myData").html(result);
            },
            error: function (msg) {
                alert(msg.toSource());                 
            }
        });
    });