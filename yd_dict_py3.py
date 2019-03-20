#!/home/porter/anaconda3/bin python3.5
# -*- coding: utf-8 -*-

import requests
from lxml import etree
from sys import argv


#---!/usr/bin/env python3
# sss-*- coding: utf-8 -*-

URL = "http://dict.youdao.com/w/eng/{}/#keyfrom=dict2.index"


def translate(words):
    """函数说明：
    因为采用 get 方式 url 中要过滤掉 / 换成全角。否则引起url的解析错误。
    response.text 是 bytes 数据类型
    """
    #headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36'}
    #headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/70.0.3538.67 Chrome/70.0.3538.67 Safari/537.36'}
    # headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/70.0.3538.67 Chrome/70.0.3538.67 Safari/537.36'}
    words = words.replace("/", "／")
    url = URL.format(words)

    response = requests.get(url)
    selector = etree.HTML(response.text)     # 生成 selector  对象, 利用 xpath 获得内容
    # content = selector.xpath("//div[@id='results-contents']")[0]
    content = selector.xpath("//div[@id='container']")[0]
    content = etree.tostring(content, encoding='utf-8', method='html')

    result = content.decode('utf-8')

    # 添加单词发音功能，但是这里，我网页中调试有道网页也不能发音，所以直接美式发音和英式发音都搞成一样的美式发音，待解决
    result = result.replace("<div class=\"trans-container\">", "<div class=\"trans-container\"><audio style=\"height: 40px; width: 66%;\" src=\"http://dict.youdao.com/dictvoice?audio=" +words+"\" controls=\"controls\">Your browser does not support the audio element.</audio><br />"+"<div class=\"trans-container\">")       # url 方式要过滤掉 / 换成全角
    # 替换爬出的网页内部rel跳转不了的问题，直接用href链接过去。
    result = result.replace("<a rel=\"#", "<a href=\"#");
    return result


if __name__ == "__main__":
    """
    argv[1] 获得控制器输入的第一个参数
    """
    result = translate(argv[1])

    # 添加网页的头文件包含有道云词典的js和css样式脚本。
    result = "<head>\n<link rel=\"stylesheet\" type=\"text/css\" href=\"https://shared.ydstatic.com/dict/v2016/result/160621/result-min.css\" />\n</head>\n<body class =\"t0\">" \
    +"<link rel=\"stylesheet\" type=\"text/css\" href=\"https://shared.ydstatic.com/dict/v2016/result/pad.css\" />\n</head>\n<body class =\"t0\">\n" \
    +"\n<script src=\"https://shared.ydstatic.com/dict/v2016/result/160621/result-wordArticle.js\"></script>\n" \
    +"<script type=\"text/javascript\" src=\"https://shared.ydstatic.com/dict/result/v2018/180927/result-min.js\"></script>\n" \
    +"<script type=\"text/javascript\" src=\"https://shared.ydstatic.com/dict/v2016/160525/autocomplete_json.js\"></script>\n" \
    +"<script type=\"text/javascript\" src=\"https://shared.ydstatic.com/js/rlog/v1.js\"></script>\n" \
    +"<script type=\"text/javascript\" src=\"https://shared.ydstatic.com/js/jquery/jquery-1.8.2.min.js\"></script>\n" \
    +"<script type=\"text/javascript\" src=\"https://cdn.staticfile.org/jquery/1.9.1/jquery.min.js\"></script>\n" \
    +"<script type=\"text/javascript\" src=\"https://shared.ydstatic.com/dict/v5.15/scripts/picugc-min6.js\"></script>\n" \
    +result+"</body>" \
    +"<style type=\"text/css\">#yddContainer{display:block;font-family:Microsoft YaHei;position:relative;width:100%;height:100%;top:-4px;left:-4px;font-size:12px;border:1px solid}#yddTop{display:block;height:22px}#yddTopBorderlr{display:block;position:static;height:17px;padding:2px 28px;line-height:17px;font-size:12px;color:#5079bb;font-weight:bold;border-style:none solid;border-width:1px}#yddTopBorderlr .ydd-sp{position:absolute;top:2px;height:0;overflow:hidden}.ydd-icon{left:5px;width:17px;padding:0px 0px 0px 0px;padding-top:17px;background-position:-16px -44px}.ydd-close{right:5px;width:16px;padding-top:16px;background-position:left -44px}#yddKeyTitle{float:left;text-decoration:none}#yddMiddle{display:block;margin-bottom:10px}.ydd-tabs{display:block;margin:5px 0;padding:0 5px;height:18px;border-bottom:1px solid}.ydd-tab{display:block;float:left;height:18px;margin:0 5px -1px 0;padding:0 4px;line-height:18px;border:1px solid;border-bottom:none}.ydd-trans-container{display:block;line-height:160%}.ydd-trans-container a{text-decoration:none;}#yddBottom{position:absolute;bottom:0;left:0;width:100%;height:22px;line-height:22px;overflow:hidden;background-position:left -22px}.ydd-padding010{padding:0 10px}#yddWrapper{color:#252525;z-index:10001;background:url(chrome-extension://eopjamdnofihpioajgfdikhhbobonhbb/ab20.png);}#yddContainer{background:#fff;border-color:#4b7598}#yddTopBorderlr{border-color:#f0f8fc}#yddWrapper .ydd-sp{background-image:url(chrome-extension://eopjamdnofihpioajgfdikhhbobonhbb/ydd-sprite.png)}#yddWrapper a,#yddWrapper a:hover,#yddWrapper a:visited{color:#50799b}#yddWrapper .ydd-tabs{color:#959595}.ydd-tabs,.ydd-tab{background:#fff;border-color:#d5e7f3}#yddBottom{color:#363636}#yddWrapper{min-width:250px;max-width:400px;}</style>"
    

    print(result)
    # 直接发音
    # playsound('http://dict.youdao.com/dictvoice?audio='+argv[1])
