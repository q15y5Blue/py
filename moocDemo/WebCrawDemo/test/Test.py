#coding:utf8
import re
strTest="""<p>用微信扫码二维码</p> <p>分享至好友和朋友圈</p> <p class="otitle">
（原标题：玉溪一骑“黑车”女子被民警当孩子面殴打？警方：辅警制止打电话时发生肢体冲突）
</p> <p><!--enpproperty 4878947</articleid><date>2017-07-09 10:37:54.0</date></author><title>玉溪一骑“黑车”女子被民警当孩子面殴打？</p><p>警方：辅警制止打电话时发生肢体冲突</title><keyword>玉溪,殴打妇女,民警</keyword><siteid>2</siteid><nodeid>6350</nodeid><nodename>云南看点</nodename>/enpproperty--></p> <p class="f_center"><img align="center" alt="玉溪一骑“黑车”女子被民警当孩子面殴打？警方：辅警制止打电话时发生肢体冲突" id="6653747" src="http://cms-bucket.nosdn.127.net/catchpic/4/4c/4c4f5dc937634ee14fbe506150b5591a.png?imageView&amp;thumbnail=550x0"/></p> <p class="f_center"><span style="text-align: justify;">网友“扎扎.克拉拉”发的贴文</span></p> <p class="f_center"><img align="center" alt="玉溪一骑“黑车”女子被民警当孩子面殴打？警方：辅警制止打电话时发生肢体冲突" id="6653748" src="http://cms-bucket.nosdn.127.net/catchpic/1/19/1908708e05f1523cb959f74a9b819c38.jpg?imageView&amp;thumbnail=550x0"/></p> <p class="f_center"><span style="text-align: justify;">网友“扎扎.克拉拉”发的贴文</span></p> <p>云南网讯 近日，有网友发帖称，玉溪市公安局红塔山派出所民警在街头盘查处置一辆被盗电摩托时，当着4岁孩子的面动手打了一名骑车女子，引发大量网友关注和热议。7月9日，当地警方回应称，现场辅警欲对可疑车辆进行进一步检查时，涉事女子不愿意配合，并要打电话联系相关人员，为不影响调查工作，不允许她打电话，在制止过程中双方发生肢体冲突。目前双方已自行和解。</p> <p><strong>网友发帖：“民警在沃尔玛门口当着孩子的面殴打妇女”</strong></p> <p>7月8日，网友“扎扎.克拉拉”在网上发帖称，7月6日下午，其表妹4岁的儿子因牙疼一直哭闹，所以向朋友借了一辆电摩托以后就载他去看牙医。在当地沃尔玛前门时，有4名自称是红塔山派出所的民警说，这辆电摩托喷漆痕迹严重，怀疑是被盗车辆，其表妹按照民警的要求配合看了车架号，民警打电话核实以后确定电摩托为被盗车辆，要将表妹拷回派出所，随后她解释说车不是自己的，先打个电话给借给自己车的人，但民警认定其表妹就是盗车人所以不允许她打电话。</p> <p>据网友“扎扎.克拉拉”介绍，在此过程中，其中一名民警抢夺表妹的手机，并当着其孩子的面抬手就给了她一巴掌，“表妹当时特别气愤，抬脚给了打他一巴掌呢男人一脚，踢在大腿上，这个男人就更不得了，揪的我表妹呢头发又给了她一巴掌。”最后，她被打后出现头昏眼花、嘴角流血等症状，孩子受到了惊吓。其表妹被带到红塔山派出所后，在民警调取的监控录像中，只播放了其表妹还手时的录像，而民警打人的整个过程都没有放。“从带到派出所以后，打人的民警就没有露过面。”</p> <p>当电摩托的车主来了以后，承认自己买的是一辆“黑车”，电摩托随即被警方扣下。随后，民警告诉表妹可以回家了，随时等电话通知，但她一直不肯走，熬了近两个小时左右，打人的民警迫不得已才出来道歉。</p> <p><strong>警方回应：对可疑车辆进行检查时双方发生肢体冲突</strong></p> <p>7月9日上午，云南网从玉溪市公安局红塔分局了解到，7月6日下午7点50分左右，针对沃尔玛周边“两车”（摩托车、电动自行车）被盗时有发生的现象，红塔山派出所带班领导安排民警带巡防队员，到沃尔玛周边开展便衣蹲守，发现一妇女张某某（女，27岁，宣威市人）推一辆新喷过漆的电动自行车行走时，该车有被盗抢车辆的嫌疑。此时，民警因其他警情已离开现场，四名辅警表明身份并出示了工作证件后，提出对可疑车辆进行检查，经查验后发现，该电动车是今年3月29日被盗的车辆，玉兴派出所已立案。</p> <p>通报称，辅警对被盘查妇女说明情况后，要求她配合调查，前往红塔山派出所再进一步落实情况，张某某不愿意配合，并要打电话联系相关人员。为不影响调查工作，工作人员不允许她打电话。盘查对象不听劝告，制止过程中，张动手打了工作人员胸口一拳后，辅警还手在对方脸上打了一巴掌，由此，双方发生肢体冲突。随后，110巡逻车赶到现场，将张带回到红塔山派出所进一步调查后查实。经查，该车确实是张向其友罗某某（女，31岁，新平县人）借用的。警方找到罗某某后，了解到该车是其在今年4月11日在龙马大酒店附近向一名陌生男子低价购买而得。案件还在进一步调查中。</p> <p><!-- AD200x300_2 -->
<div class="gg200x300">
<div style="position:relative;">
<a class="ad_hover_href" href="http://gb.corp.163.com/gb/legal.html"></a>
<iframe border="0" frameborder="no" height="250" marginheight="0" marginwidth="0" scrolling="no" src="http://g.163.com/r?site=netease&amp;affiliate=news&amp;cat=article&amp;type=logo300x250&amp;location=12" width="300"> </iframe>
</div>
</div><p>当晚，冲突双方在红塔山派出所带班领导见证参与下，已进行了自行和解，张某某对自己的冲动行为，首先表示后悔并向警方表达了歉意，动手的协警也因自己工作中存在不文明的行为，随后向对方诚恳地表示道歉。</p><p>事件发生后，针对辅警工作中的不文明行为，红塔山派出所分管领导非常重视，已组织全体辅警人员以会代训，进一步开展再教育、再培训，再强调，以此为例引以为戒，在今后的工作中，坚决杜绝再次发生类似不文明行为。</p><p>云南网注意到，对于警方的上述回应，网友“扎扎.克拉拉”表示，要求公开监控视频，一切用事实说话。</p>
<p></p>
<div class="ep-source cDGray">
<span class="left"><a href="http://news.163.com/"><img alt="王征" class="icon" height="12" src="http://img1.cache.netease.com/cnews/css13/img/end_news.png" width="13"/></a> 本文来源：云南网  作者：熊强</span>
<!--王征_B7526--><span class="ep-editor">责任编辑：王征_B7526</span> </div>
</p> <p>当晚，冲突双方在红塔山派出所带班领导见证参与下，已进行了自行和解，张某某对自己的冲动行为，首先表示后悔并向警方表达了歉意，动手的协警也因自己工作中存在不文明的行为，随后向对方诚恳地表示道歉。</p> <p>事件发生后，针对辅警工作中的不文明行为，红塔山派出所分管领导非常重视，已组织全体辅警人员以会代训，进一步开展再教育、再培训，再强调，以此为例引以为戒，在今后的工作中，坚决杜绝再次发生类似不文明行为。</p> <p>云南网注意到，对于警方的上述回应，网友“扎扎.克拉拉”表示，要求公开监控视频，一切用事实说话。</p> <p></p> <p>用微信扫码二维码</p> <p>分享至好友和朋友圈</p> <p class="piao_art_p"><a href="http://piao.163.com/#from=artfoot" target="_blank">特价影票4折起</a><a href="http://piao.163.com/beijing/cinema/area-0-page-1-keywords-.html#from=artfoot" target="_blank">在线选座</a></p> <p class="piao_art_p"><a href="http://piao.163.com/iphone.html#from=artfoot" target="_blank">iphone客户端</a><a href="http://piao.163.com/android.html#from=artfoot" target="_blank">安卓客户端</a></p> <p>
</p>"""

regex="""<p>.*?</p>"""
t=re.findall(regex,strTest)
print(t)
m=re.search(regex,strTest)
print(m)