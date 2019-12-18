import requests
import json
import re
import os
import urllib
from lxml import etree


# 评论用户基本信息
class User:
    def __init__(self, id=0, name='无', face='无'):
        # 用户id
        self.uid = id
        # 用户昵称
        self.uname = name
        # 用户头像
        self.uface = face


# 评论
class Comment:
    def __init__(self, user, date, msg='无', like=0, reply=0):
        # 评论用户
        self.user = user
        # 评论内容
        self.msg = msg
        # 评论日期
        self.date = date
        # 点赞数
        self.like = like
        # 回复数
        self.reply = reply


# 获取get请求响应内容
def get_response(url):
    COOKIE = 'SINAGLOBAL=4311943425583.0225.1568427385347; un=15208159422; wvr=6; SUBP=0033WrSXqPxfM72' \
             '5Ws9jqgMF55529P9D9W56r5woK0fcRiNXOHAbjj0I5JpX5KMhUgL.Fo-c1heRShqpeh22dJLoI05LxK-LB-BLBKBLx' \
             'KML12zLB-eLxKML1-2L1hBLxKqLBK5LBo.LxK-L12qLBoMcSh-t; ALF=1608168309; SCF=ArCtoPVcYR-3GBiAD' \
             'XGTzfgnmjFtZb1s55ahEYJzpz8xUfKnYFeQFsTHcyovb650POoKHt9a1myR7jf0sSaQqLw.; SUHB=0ebtJ1LQdOI_' \
             '9H; UOR=www.takefoto.cn,widget.weibo.com,login.sina.com.cn; wb_view_log_5683846101=1920*108' \
             '01; Ugrow-G0=5c7144e56a57a456abed1d1511ad79e8; SUB=_2A25w_YNcDeRhGeNI41EZ9CjNyz2IHXVTivOUrD' \
             'V8PUNbn9AKLUPykW9NSDJvpoANzWTfxYiAl42d8pBBLLE0Zl6x; YF-V5-G0=e8fcb05084037bcfa915f5897007cb' \
             '4d; _s_tentry=login.sina.com.cn; Apache=6977668431281.743.1576661779704; ULV=1576661779751:' \
             '6:5:4:6977668431281.743.1576661779704:1576632316030; YF-Page-G0=20a0c65c6e2ee949c1f78305a122' \
             '073b|1576661812|1576661779; TC-V5-G0=eb26629f4af10d42f0485dca5a8e5e20; webim_unReadCount=%7B' \
             '%22time%22%3A1576661979008%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allco' \
             'untNum%22%3A18%2C%22msgbox%22%3A0%7D; TC-Page-G0=45685168db6903150ce64a1b7437dbbb|1576661989|' \
             '1576661989'
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/74.0.3729.169 Safari/537.36 '
    REFERER = 'https://weibo.com/u/3176010690?refer_flag=1001030103_&is_all=1'
    header = {
        'User-Agent': USER_AGENT,
        'REFERER': REFERER,
        'Cookie': COOKIE
    }
    get_rsp = requests.get(url, headers=header)
    get_rsp.encoding = "utf-8"
    return get_rsp.text


# 获取post请求响应内容
def post_response(url, form):
    header = {
        'Host': 'www.lagou.com',
        'Origin': 'https://www.lagou.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.lagou.com/jobs/list_Java?px=default&gx=%E5%AE%9E%E4%B9%A0&gj=&isSchoolJob=1&city=%E6%88%90%E9%83%BD',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'X-Anit-Forge-Token': 'None',
        'X-Anit-Forge-Code': '0',
        'Content-Length': '23',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'X-Anit-Forge-Code': '0',
        'X-Anit-Forge-Token': 'None',
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': '_ga=GA1.2.1624671375.1529386613; _gid=GA1.2.314178163.1529386613; user_trace_token=20180619133653-c5f8be61-7382-11e8-a94e-525400f775ce; LGUID=20180619133653-c5f8c20a-7382-11e8-a94e-525400f775ce; JSESSIONID=ABAAABAAADEAAFI8DA399D1C898F00FFAD24FEAF8B41BFF; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1529386613,1529421310,1529639564; X_HTTP_TOKEN=d0ab73805e04110bdf13bc639e2b2a2a; _putrc=949A7B9732130CEA123F89F2B170EADC; login=true; unick=%E8%A2%81%E5%8D%9A%E6%96%87; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; index_location_city=%E6%88%90%E9%83%BD; TG-TRACK-CODE=index_navigation; gate_login_token=3f528ff1ac4fbf8c93c13a5d3fd2cb7728cac0091291256c66e0d711ae51c0d1; LGRID=20180622135618-fb95e7cb-75e0-11e8-aca8-525400f775ce; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1529646978; SEARCH_ID=fa7ffe8120214f219a387c1fadd7eb5c'
    }
    post_rsp = requests.post(url, data=form, headers=header)
    post_rsp.encoding = 'utf-8'
    return post_rsp.text


# 单行打印
def printl(str):
    print(str, end='')


# 获取带带大师兄主页所有的动态id
# response:主页响应
def get_news_id(page_rsp):
    # 微博动态
    news_reg = re.search(r'<script>FM.view.*Pl_Official_MyProfileFeed__21.*html\":\"(.*)\"', page_rsp, re.M | re.I)
    # 获取所有微博动态html页面
    news_html_str = news_reg.group(1).replace("\\", "")
    news_html = etree.HTML(news_html_str)
    return news_html.xpath("//div[@class='WB_from S_txt2']/a/@name")


# 获取某个动态的所有评论html节点
# news_id:动态id
def get_comments_node(news_id):
    comments_url = "https://weibo.com/aj/v6/comment/big?ajwvr=6&id=" + news_id + "&from=singleWeiBo&__rnd=1576638955082"
    comments_rsp = get_response(comments_url)
    # 转json
    comments_json = json.loads(comments_rsp)['data']['html']
    comments_html = etree.HTML(comments_json)
    return comments_html


# 获取某个动态的所有评论id
# comments_html:评论节点
def get_comments_id(comments_html):
    return comments_html.xpath("//div[@class='list_ul']/div/@comment_id")


# 根据comment_id获取某个评论的信息
# comment_id:评论id
# comments_html:评论节点
def get_comment_info(comments_html, comment_id):
    prefix = "//div[@comment_id='" + comment_id + "']"
    uid = re.sub(r'\D', '',
                 str(comments_html.xpath(prefix + "/div[@class='list_con']/div[@class='WB_text']/a[1]/@usercard")))
    uname = comments_html.xpath(prefix + "/div[@class='list_con']/div[@class='WB_text']/a[1]/text()")[0]
    uface = comments_html.xpath(prefix + "/div[@class='WB_face W_fl']/a[1]/img/@src")[0]
    date = comments_html.xpath(
        prefix + "/div[@class='list_con']/div[@class='WB_func clearfix']/div[@class='WB_from S_txt2']/text()")
    msg = comments_html.xpath(prefix + "/div[@class='list_con']/div[@class='WB_text']/text()")[1]
    like = comments_html.xpath(
        prefix + "/div[@class='list_con']/div[@class='WB_func clearfix']/div[@class='WB_handle W_fr']/ul[@class='clearfix']/li[last()]/span/a/span/em[last()]/text()")[
        0]
    reply = re.sub(r'\D', '', str(comments_html.xpath(
        prefix + "/div[@class='list_con']/div[@class='list_box_in S_bg3']/div[@class='list_ul']/div[@class='list_li_v2']/div[@class='WB_text']/a[last()]/text()")))
    # 封装
    user = User(uid, uname, uface)
    # 最后封装为Comment类并返回
    comment = Comment(user, date, msg, like, reply)
    return comment


# 通过动态id和评论id查询对应评论的回复
# 图片从此处获取
def get_comment_reply(news_id, comment_id):
    reply_url = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&more_comment=big&root_comment_id=' + comment_id + '&is_child_comment=ture&id=' + news_id + '&from=singleWeiBo&__rnd=1576676691568 '
    reply_rsp = get_response(reply_url)
    # 转json
    reply_json = json.loads(reply_rsp)['data']['html']
    reply_html = etree.HTML(reply_json)
    reply_msg = reply_html.xpath("//div[@class='WB_text']/a/@alt")
    return reply_msg


if __name__ == '__main__':
    # 带带大师兄的主页
    URL = "https://weibo.com/u/3176010690?is_all=1"
    response = get_response(URL)
    news_id = get_news_id(response)
    printl("主页所有动态id:")
    print(news_id)
    print('-----------')
    # 获取所有评论节点
    comment_node = get_comments_node(news_id[1])
    printl("动态id为" + news_id[1])
    printl("的所有评论节点:")
    print(comment_node)
    # 获取所有评论id数组
    comments_id = get_comments_id(comment_node)
    print('-----------')
    printl("动态id为" + news_id[1])
    printl("的所有评论id数组:")
    print(comments_id)
    print('-----------')
    for id in comments_id:
        # 通过comment_id获取某个评论信息
        comment_info = get_comment_info(comment_node, id)
        printl("动态id为" + news_id[1])
        printl(",评论id为")
        printl(id)
        printl("的评论信息为:")
        print(comment_info.msg)
    printl("动态id为4450865186446461")
    print(",评论id为4450865274203845的回复为")
    print(get_comment_reply('4450865186446461', '4450865274203845'))
    # pic = get_response('http://t.cn/AiDeXfdu')
    # printl(pic)
    urllib.request.urlretrieve('https://wx1.sinaimg.cn/bmiddle/0063M2h7ly1ga0w3d7ueaj30u01sz107.jpg', "{}{}.jpg".format('F:\\doPython\\weibo\\', 'a'))
    # result = json.loads(response)
    # print(result)
    # # 第一次点击评论条数所显示的评论
    # main_page_comment_result = result["data"]["html"]
    # main_page_comment_html = etree.HTML(main_page_comment_result)
    # main_page_comment_html.xpath("//div[@class='WB_text']/text()")
    # # 用于从评论中找无内鬼的正则
    # neigui_reg = re.compile("无内鬼")
    # # 第几个WB_text
    # comment_index = 0
    # # 无内鬼评论出现的评论坐标
    # neigui_index = []
    # # 遍历找无内鬼
    # for comment in main_page_comment_html.xpath("//div[@class='WB_text']/text()"):
    #     comment_index += 1
    #     if neigui_reg.search(comment):
    #         neigui_index.append(comment_index)
    # print(neigui_index)
    # # 评论页面响应结果
    # comment_response = result["data"]["html"]
    # # 将响应变成完整页面
    # comment_html = etree.HTML(comment_response)
    # # 所有评论
    # comment_list = comment_html.xpath("//div[@class='list_ul']/div/@comment_id")
    # print(comment_list)
