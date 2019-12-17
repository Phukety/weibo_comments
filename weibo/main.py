import requests
import json
import re
import os
from lxml import etree
import urllib


# 获取get请求响应内容
def get_response(url):
    COOKIE = 'SINAGLOBAL=2679365301321.8276.1553576292987; un=15208159422; UOR=www.baidu.com,weibo.com,' \
             'login.sina.com.cn; wvr=6; Ugrow-G0=5c7144e56a57a456abed1d1511ad79e8; ' \
             'YF-V5-G0=b588ba2d01e18f0a91ee89335e0afaeb; _s_tentry=login.sina.com.cn; ' \
             'Apache=2763084705464.9575.1576593181302; wb_view_log_5683846101=1920*10801; ' \
             'ULV=1576593181494:3:3:3:2763084705464.9575.1576593181302:1576508352858; ' \
             'login_sid_t=e4c43d5919120eda49f78dc7a3847b0e; cross_origin_proto=SSL; wb_view_log=1920*10801; ' \
             'WBtopGlobal_register_version=307744aa77dd5677; ' \
             'SCF=AomUhaoj-mPwbu8pvNzRbles3nTnnWPAocOC7fkH1EluiurAsLr7MxnKo6FbjUoAsZX1uw9BIvIGaxk3M4pFf90.; ' \
             'SUB=_2A25w_JfeDeRhGeNI41EZ9CjNyz2IHXVTi44WrDV8PUNbmtAfLVLckW9NSDJvpmOO9xRHZPQkgLOTpeyTbAkt34XM; ' \
             'SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W56r5woK0fcRiNXOHAbjj0I5JpX5K2hUgL.Fo-c1heRShqpeh22dJLoI05LxK-LB' \
             '-BLBKBLxKML12zLB-eLxKML1-2L1hBLxKqLBK5LBo.LxK-L12qLBoMcSh-t; SUHB=03oF1iG0eoSOrJ; ALF=1577198092; ' \
             'SSOLoginState=1576593294; YF-Page-G0=7f483edf167a381b771295af62b14a27|1576594465|1576594327; ' \
             'webim_unReadCount=%7B%22time%22%3A1576594472050%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0' \
             '%2C%22allcountNum%22%3A14%2C%22msgbox%22%3A0%7D '
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


if __name__ == '__main__':
    URL = "https://weibo.com/aj/v6/comment/small?ajwvr=6&act=list&mid=4450179569135215&uid=5683846101&isMain=true" \
          "&dissDataFromFeed=%5Bobject%20Object%5D&ouid=3176010690&location=page_100505_home&comment_type=0&_t=0" \
          "&__rnd=1576508872952 "
    response = get_response(URL)
    result = json.loads(response)
    print(result)
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
    # 评论页面响应结果
    comment_response = result["data"]["html"]
    # 将响应变成完整页面
    comment_html = etree.HTML(comment_response)
    # 所有评论
    comment_list = comment_html.xpath("//div[@class='list_ul']/div/@comment_id")
    print(comment_list)
