title=天池阿里音乐流行趋势预测大赛
en_title=alimusic
category=DataMining
tags=DataMinning,AliTianchi
summary=为期两个月的天池阿里音乐大数据竞赛终于落下帷幕，两个月走来无数次的激动，无数次绝望，好在一路走来，所有已经尘埃落定，第六名的尴尬成绩，让我等既参加不了决赛，也没有什么好值得吹牛逼的。本着程序猿的分享精神，我会结合团队中队友的思路，将整个比赛的结题方法share给大家，望各位太君去粗取精，有不正确的地方还望批评指正。
<ep_info>
#天池阿里音乐流行趋势预测大赛
####☛<font color=red>想要干货直接忽略这部分</font>☚

<pre class="brush:cpp;">
model = RandomForestRegressor(n_jobs=-1,
	n_estimators=100,
	max_features=5,#5
	max_depth=8,#8
	min_samples_leaf=2,
	random_state=219)
</pre>
