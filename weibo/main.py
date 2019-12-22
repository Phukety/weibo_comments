import requests
import json
import re
import urllib
import time
import schedule
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

    def print_user(self):
        print("用户信息:用户编号uid={},用户昵称uname={},用户头像uface={}".format(self.uid, self.uname, self.uface))


# 动态
class News:
    def __init__(self, user='无', id=0, date="", msg=""):
        # 动态id
        self.nid = id
        # 动态发送用户
        self.nuser = user
        # 动态发布日期
        self.ndate = date
        # 动态文字内容
        self.nmsg = msg

    def print_news(self):
        self.nuser.print_user()
        print("动态信息:动态编号nid={},动态发布日期ndate={},动态文字内容nmsg={}".format(self.nid, self.ndate, self.nmsg))


# 评论
class Comment:
    def __init__(self, cid=0, user='无', date='无', msg='无', like=0, reply=0):
        # 评论id
        self.cid = cid
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

    def print_comment(self):
        self.user.print_user()
        print("评论信息:评论编号cid={},评论内容msg={},评论日期date={},点赞数like={},回复数reply={}".format(self.cid, self.msg, self.date,
                                                                                     self.like, self.reply))


# 获取get请求响应内容
def get_response(url):
    COOKIE = 'SINAGLOBAL=2679365301321.8276.1553576292987; un=15208159422; UOR=www.baidu.com,weibo.com,' \
             'login.sina.com.cn; wvr=6; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W56r5woK0fcRiNXOHAbjj0I5JpX5KMhUgL.Fo' \
             '-c1heRShqpeh22dJLoI05LxK-LB-BLBKBLxKML12zLB-eLxKML1-2L1hBLxKqLBK5LBo.LxK-L12qLBoMcSh-t; ' \
             'ULV=1576904827459:5:5:5:4282834670867.1284.1576904827438:1576676474862; ' \
             'Ugrow-G0=140ad66ad7317901fc818d7fd7743564; ALF=1608530350; SSOLoginState=1576994352; ' \
             'SCF=AomUhaoj-mPwbu8pvNzRbles3nTnnWPAocOC7fkH1EluwZqvfpq4RNbzwfG4bvvpEHs-nv_bstW-lXFAxwKeSm8.; ' \
             'SUB=_2A25w-3ZgDeRhGeNI41EZ9CjNyz2IHXVQceCorDV8PUNbmtAfLWH_kW9NSDJvplX7rHRJzjxa0FLbCWVR_IMRqbnm; ' \
             'SUHB=0oUoUlkh8bS3cO '
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
def get_news_info(page_rsp):
    # 微博动态
    news_reg = re.search(r'<script>FM.view.*Pl_Official_MyProfileFeed__21.*html\":\"(.*)\"', page_rsp, re.M | re.I)
    # 获取所有微博动态html页面
    news_html_str = news_reg.group(1).replace("\\", "")
    news_html = etree.HTML(news_html_str)
    # 用户id
    uid = re.search('id=(.*)&type', str(news_html.xpath("(//div[@class='WB_info'])[1]/a[1]/@usercard")[0])).group(1)
    # 用户name
    uname = news_html.xpath("(//div[@class='WB_info'])[1]/a[1]/text()")[0]
    # 用户头像
    uface = news_html.xpath("(//div[@class='WB_face W_fl'])[1]/div[@class='face']/a[1]/img/@src")[0]
    # news_html.xpath("//div[@class='WB_from S_txt2']/a/@name")
    user = User(uid, uname, uface)
    # 动态数组
    news = []
    # 动态个数
    news_num = len(news_html.xpath("//div[@action-type='feed_list_item']"))
    for i in range(1, news_num + 1):
        # 每一个动态的html
        index = str(i + 1)
        each_news = news_html.xpath(
            "(//div[@class='WB_feed WB_feed_v3 WB_feed_v4']/div['WB_cardwrap WB_feed_type S_bg2 WB_feed_like '])[" + index + "]")[
            0]
        # 获取动态id
        nid = each_news.xpath(".//@mid")[0]
        # 获取动态内容
        nmsg = str(' '.join(each_news.xpath(".//div[@class='WB_text W_f14']/text()"))).replace(" ", "").replace("n", "")
        # 获取发布日期
        ndate = each_news.xpath(".//div[@class='WB_from S_txt2']/a[1]/@title")[0]
        news_info = News(user, nid, ndate, nmsg)
        news.append(news_info)
    return news


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
    uface = comments_html.xpath(prefix + "/div[@class='WB_face W_fl']/a[1]/img/@src")
    date = comments_html.xpath(
        prefix + "/div[@class='list_con']/div[@class='WB_func clearfix']/div[@class='WB_from S_txt2']/text()")[0]
    msg = comments_html.xpath(prefix + "/div[@class='list_con']/div[@class='WB_text']/text()")[1]
    like = comments_html.xpath(
        prefix + "/div[@class='list_con']/div[@class='WB_func clearfix']/div[@class='WB_handle W_fr']/ul[@class='clearfix']/li[last()]/span/a/span/em[last()]/text()")[
        0]
    reply = re.sub(r'\D', '', str(comments_html.xpath(
        prefix + "/div[@class='list_con']/div[@class='list_box_in S_bg3']/div[@class='list_ul']/div[@class='list_li_v2']/div[@class='WB_text']/a[last()]/text()")))
    # 封装
    user = User(uid, uname, uface)
    # 最后封装为Comment类并返回
    comment = Comment(comment_id, user, date, msg, like, reply)
    return comment


# 通过动态id和评论id查询对应评论的回复
# 回复中的图片评论url从此处获取
# page-页数
# news_id-动态id
# comment_id-评论id
def get_comment_reply(page, news_id, comment_id):
    # reply_url = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&more_comment=big&root_comment_id=' + comment_id + '&is_child_comment=ture&id=' + news_id + '&from=singleWeiBo&__rnd=1576676691568 '
    reply_url = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&more_comment=big&child_comment_max_id=&child_comment_max_id_type=0&' \
                'child_comment_ext_param=&child_comment_page={}&is_child_comment=true&' \
                'root_comment_id={}&child_comment_id=&last_child_comment_id=&' \
                'id={}&from=singleWeiBo&__rnd=1576733854666'.format(page, comment_id, news_id)
    reply_rsp = get_response(reply_url)
    # 转json
    reply_json = json.loads(reply_rsp)['data']['html']
    reply_html = etree.HTML(reply_json)
    # 回复中图片的action_data
    reply_pic_action_data = reply_html.xpath("//div[@class='list_con']/div[@class='WB_text']/a/@action-data")
    # 取object_id正则表达式
    pid_reg = re.compile('object_id=(.*)&pid')
    # 存图片地址
    pic = []
    # 遍历并用正则取出图片的object_id
    for action_data in reply_pic_action_data:
        # 解析object_id
        object_id = pid_reg.search(action_data).group(1)
        pic.append(get_pic_src(object_id))
    return pic


# 通过图片object_id发送请求获取图片地址
# 不直接用pid组装图片地址的原因是图片有些是git图,为了找到后缀
def get_pic_src(object_id):
    # 图片请求地址
    pic_req_url = 'https://photo.weibo.com/h5/comment/compic_id/' + object_id
    pic_req = get_response(pic_req_url)
    pic_html = etree.HTML(pic_req)
    pic_src = pic_html.xpath("//img/@src")[0]
    return pic_src


# 定时脚本
def job():
    # 带带大师兄的主页
    URL = "https://weibo.com/u/3176010690?is_all=1"
    response = get_response(URL)
    news_list = get_news_info(response)
    print("主页第一页发布的动态(取最新发布的动态):")
    # 取最新动态
    for k in range(1, 2):
        news_index = k
        first_news = news_list[news_index]
        first_news.print_news()
        # 获取动态id
        news_id = first_news.nid
        print('-----------')
        # 获取所有评论节点
        comment_node = get_comments_node(news_id)
        # 获取所有评论id数组
        comments_id = get_comments_id(comment_node)
        # 无内鬼的评论
        comment_info = Comment()
        # 找到无内鬼的评论
        for id in comments_id:
            # 通过comment_id获取某个评论信息
            comment_info = get_comment_info(comment_node, id)
            # 找到第一个无内鬼就停止
            if re.search('无内鬼', comment_info.msg):
                break
        # 打印无内鬼评论的基本信息
        comment_info.print_comment()
        # 根据回复数reply得出大概多少页数(不准确)  page=reply//15+1
        # page = int(comment_info.reply) // 15 + 1
        page = 20
        # 遍历每一页
        print("一共{}页".format(page))
        # 获取开始时间戳,单位ms
        start = int(round(time.time() * 1000))
        # 所有图片总数
        count = 0
        for i in range(1, page):
            # 获取每一页的回复中的图片地址
            printl("第{}页:".format(i))
            pic_urls = get_comment_reply(i, news_id, comment_info.cid)
            print(pic_urls)
            # 获取图片pid正则
            pid_reg = re.compile('bmiddle\/(.*)\.')
            # 图片个数
            pic_num = 0
            # 获取当页开始时间戳,单位ms
            page_start = int(round(time.time() * 1000))
            # 批量下载图片
            for pic_url in pic_urls:
                pid = re.search(pid_reg, pic_url).group(1)
                suffix = pic_url.split('.')[-1]
                print("开始下载pid={}的图片,图片名称={}.{}".format(pid, pid, suffix))
                # 下载到F:\\doPython\\weibo\\目录下
                # 获取图片pid作为图片名称
                # 获取文件后缀
                urllib.request.urlretrieve(pic_url, "{}{}.{}".format('F:\\doPython\\weibo\\', pid, suffix))
                pic_num += 1
                count += 1
            # 获取结束时间戳
            page_end = int(round(time.time() * 1000))
            print("第{}页图片下载完成,一共{}张,耗时{}ms".format(i, pic_num, page_end - page_start))
        # 获取结束时间戳,单位ms
        end = int(round(time.time() * 1000))
        print("{}页图片下载完成,一共{}张,耗时{}ms".format(page, count, end - start))


if __name__ == '__main__':
    # 每天18:00执行
    schedule.every().day.at("18:00").do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
