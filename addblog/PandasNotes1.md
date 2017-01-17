title=数据分析工具包pandas学习笔记（一）
en_title=pandas
category=ToolBox
tags=python,pandas
summary=pandas
<ep_info>

###博客参考 [10 Minutes to pandas](http://pandas.pydata.org/pandas-docs/stable/10min.html)，如有不当还请参考英文版。

#一、Introduction
一般情况下，pandas要和numpy和制图工具matplotlib一起使用。
>
	import pandas as pd
	import numpy as np
	import matplotlib.pyplot as plt

#二、创建对象
pandas的对象包括`Series`,`DataFrame`。
>####1.Series
>> `s = pd.Series([1,3,5,np.nan,6,8])`
>####2.DataFrame
>>创建一个以时间为索引的被标记的表
>
>>     dates = pd.date_range('20130101', periods=6)
	df = pd.DataFrame(np.random.randn(6,4), index=dates, columns=list('ABCD'))
>>通过`df`可以看到最后的输出为
>
>>                 A        B         C         D
	2013-01-01  0.469112 -0.282863 -1.509059 -1.135632
	2013-01-02  1.212112 -0.173215  0.119209 -1.044236
	2013-01-03 -0.861849 -2.104569 -0.494929  1.071804
	2013-01-04  0.721555 -0.706771 -1.039575  0.271860
	2013-01-05 -0.424972  0.567020  0.276232 -1.087401
	2013-01-06 -0.673690  0.113648 -1.478427  0.524988
>当然也可以通过字典自行定义每一列的值
>
>>`df2 = pd.DataFrame({'Key':Value})`

#三、查看数据
一下所有都是在DataFrame下的方法或者属性
>1. 查看前X或者后X个数据：`.head(X)`，`.tail(X)`;
>2. 查看索引，列名，数据：`.index`，`.columns`，`.values`；
>3. 数据的简单描述，包括个数，平均值，方差，最大最小：`.describe()`；
>4. 转置： `.T`；
>5. 按行排序，按列排序:`.sort_index(axis=axis_num, ascending=False)`，`.sort_values(by=column_name)`


#四、获取，设置数据
Setting Data相对简单，就是把DataFrame当成一个多维数组，这个数组可以使用index或者列名进行选中，然后进行数据更新或者添加。当数据量不足时，会填充NaN。
使用`.isin()`选取列是字符串的行。eg.`df[df['E'].isin(['two','four'])]`

各位太君，你能想到的最直接的方式，就可以在pandas中获取数据
eg.`df['A']`，这里需要指出的是当这个参数`'A'`的位置为一个key事，返回的是一列，当时区间`X:Y`时 返回的行，`X`，`Y`可以是整数，返回区间内的行，如果是字符串，返回index区间内的数据。

>####.loc()
>>使用`.loc()`方法就是把DataFrame当成一个多维的数组，可以通过`[[区间]，[keys, ...]]`获取DataFrame里面的数据

>####.iloc()
>>此方法将DataFrame完全视为多维的数字，通过区间进行数据访问。

>####布尔型索引
>>将满足一定条件的数据行或者列进行选取，eg.`df[df.A > 0]`会选取列名为`A`并且值大于0的那些行。


#五、数据丢失
在任何情况下数据丢失都是很正常的，这时候数据所在的位置会被填充上NaN，这时如果想要获得没有NaN的行可以使用`.dropna(how = 'any')`，使用`fillna(value=)`填充数据。

#六、操作
向DF追加行使用`.append()`函数
>####1. Join
>>这是与数据库很像的地方，可以对多个表进行连接操作.
>
>>     left = pd.DataFrame({'key': ['foo', 'foo'], 'lval': [1, 2]})
	right = pd.DataFrame({'key': ['foo', 'foo'], 'rval': [4, 5]})
	pd.merge(left, right, on='key')

>####2.Group
>> `df.groupby(args).sum()`这里面args可以是一个字符串代表要group的列或者是一个string list表示要group多列。

>####3.设置类别
>>有的时候我们经常需要将某些值设定为一些类别，例如将11点之前设置为上午，11点到1点设置为中午等等，这时候就可以将不同的时间段设置为指定的为别名。
>
>>     df = pd.DataFrame({"id":[1,2,3,4,5,6], "raw_grade":['a', 'b', 'b', 'a', 'a', 'e']})
	df["grade"] = df["raw_grade"].astype("category")
	df["grade"].cat.categories = ["very good", "good", "very bad"]

#七、显示数据
使用`.plot()`，`plt.show()`即可以显示二维图像。