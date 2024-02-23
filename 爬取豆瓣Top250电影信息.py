# coding=utf-8
'''
 @Project: 爬虫作业
@File  : 爬取豆瓣Top250电影信息.py
@Author: 于舒洋
@Desc :
@Date  :  2024/02/23
'''





#1.获取豆瓣top250网页的HTML源码
import urllib.request,urllib.error
def getUrl_Html(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }
    html = ""
    try:
        request = urllib.request.Request(url=url, headers=head)
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")

    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    # print(html)
    # html = html.encode('GBK', 'ignore').decode('GBK')
    return html

import re
#设置正则表达式
module_movielink = re.compile(r'<a href="(.*?)">')
module_PicLink = re.compile(r'<img alt=".*src="(.*?)"',re.S)
module_movieName = re.compile(r'<span class="title">(.*)</span>')
module_movieIntroduc = re.compile(r'<span class="inq">(.*?)。</span>')
module_movieRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
module_judgeNum = re.compile(r'<span>(.*?)人评价</span>')
module_movieInfo = re.compile(r'<p class="">(.*?)</p>',re.S)

#2.解析网页HTML源码
from bs4 import BeautifulSoup
def getDatalist(baseurl):
    datalist = []
    for i in range(0,10):
        html = getUrl_Html(baseurl+str(i*25))


    #格式化html
        soup = BeautifulSoup(html,"html.parser")
    # t_list = soup.find_all("div", class_="item")
        for content in soup.find_all("div", class_="item"):
            oneData = []  # 保存一部电影信息
            content = str(content)

            movielink = re.findall(module_movielink,content)[0]  #电影详情链接
            # print(movielink)
            oneData.append(movielink)

            PicLink = re.findall(module_PicLink,content)[0]    #电影图片链接
            # print(PicLink)
            oneData.append(PicLink)

            Name = re.findall(module_movieName,content)
            if len(Name) == 2:
                movieCNname = Name[0]    #电影中文名
                # print(movieCNname)
                oneData.append(movieCNname)
                movieForgname = Name[1].replace("/","").strip()
                oneData.append(movieForgname)
                # print(movieForgname)
            else:
                movieCNname = Name[0]   # 电影中文名
                oneData.append(movieCNname)
                movieForgname = ""      # 电影英文名，可为空；此处留空
                oneData.append(movieForgname)

            movieIntroduc = re.findall(module_movieIntroduc,content)  #电影简介，可为空
            if len(movieIntroduc) == 1:
                movieIntroduc = movieIntroduc[0]
                # print(movieIntroduc)
                oneData.append(movieIntroduc)
            else:
                movieIntroduc = "123"
                # print(movieIntroduc)
                oneData.append(movieIntroduc)

            rating = re.findall(module_movieRating,content)[0]     #电影评分
            # print(rating)
            oneData.append(rating)

            judgeNum = re.findall(module_judgeNum,content)[0]   #参评人数
            # print(judgeNum)
            oneData.append(judgeNum)

            movieInfo = re.findall(module_movieInfo,content)[0]  #电影信息，导演、演员、年份、电影类型
            # print(type(movieInfo))

            movieInfo = movieInfo.replace("<br/>" ,"").strip()
            movieInfo = movieInfo.replace("/","")
            movieInfo = movieInfo.replace('\n',"")
            movieInfo = movieInfo.replace('                            ', " ")
            oneData.append(movieInfo)
            datalist.append(oneData)


    print(datalist)

    # print(t_list)

    return datalist


import re
# # 影片详情链接匹配规则
# findlink = re.compile(r'<a href="(.*?)">')   #创建正则表达式对象，表示字符串匹配规则
# # 影片图片的链接匹配规则
# findImgSrc = re.compile(r'<img.*src="(.*?)"',re.S)  #re.S 让换行符包含在字符中
# # 影片的片名
# findTitle = re.compile(r'<span class="title">(.*?)</span>')
# #影片评分
# findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
# #找到评价人数
# findJudge = re.compile(r'<span>(\d*)人评价</span>')
# #找到概况
# findInq = re.compile(r'<span class="inq">(.*)</span>')
# #找到影片的相关内容
# findBd = re.compile(r'<p class="">(.*?)</p>',re.S)
# def getData(baseurl):
#     datalist = []  # 存放所有电影信息
#     for i in range(0, 10):  # 调用获取页面信息的函数，循环10次
#         url = baseurl + str(i * 25)
#         html = getUrl_Html(url)  # 保存获取到的网页源码
#         # print(html)
#         # 2.逐一解析数据
#         # datalist.append(html)
#         soup = BeautifulSoup(html, "html.parser")
#         for item in soup.find_all("div", class_="item"):
#             # print(item)   #测试查看电影item全部信息
#             data = []  # 保存一部电影的所有信息
#             item = str(item)
#
#
#             # 获取到影片详情的链接
#             link = re.findall(findlink, item)[0]  # re库用来通过正则表达式查找指定的字符串
#             data.append(link)  # 添加影片链接
#             print(data)
#             # 获取影片图片
#             ImgSrc = re.findall(findImgSrc, item)[0]
#             data.append(ImgSrc)  # 添加图片
#             # 获取影片名称
#             Titles = re.findall(findTitle, item)  # 片名可能只有一个中文名，没有外国名
#             if (len(Titles) == 2):
#                 ctitle = Titles[0]
#                 data.append(ctitle)  # 添加中文名
#                 otitle = Titles[1].replace("/", "")  # 去掉无关的符号"/"
#                 data.append(otitle)  # 添加外国名
#             else:
#                 data.append(Titles[0])
#                 data.append(' ')  # 外国名不存在时，留空
#
#             # 获取影片评分
#             rating = re.findall(findRating, item)[0]
#             data.append(rating)  # 添加评分
#
#             # 获取评价人数
#             judgeNum = re.findall(findJudge, item)[0]
#             data.append(judgeNum)  # 添加评价人数
#
#             # 获取电影概述
#             inq = re.findall(findInq, item)
#             if len(inq) != 0:
#                 data.append(inq[0].replace("。", ""))  # 添加影片概述
#             else:
#                 data.append(' ')  # 影片概述留空
#
#             # 找到影片的相关内容,导演、主演、年份等
#             bd = re.findall(findBd, item)[0]
#             bd = re.sub('<br(\s+)?/>(\s+)?', " ", bd)  # 替换<br/>
#             bd = re.sub('/', " ", bd)  # 替换 /
#             data.append(bd.strip())  # 去掉前后的空格
#
#             datalist.append(data)  # 把处理好的一部电影信息放入datalist
#     print(datalist)
#     return datalist
#3.保存解析数据到Excel


#4.保存源码数据到数据库sql


if __name__ == '__main__':
    baseurl = "https://movie.douban.com/top250?start="
    # print(baseurl+str(2*25))
    htmlInfo = getDatalist(baseurl)
    # print(htmlInfo)
    print("爬取完成")