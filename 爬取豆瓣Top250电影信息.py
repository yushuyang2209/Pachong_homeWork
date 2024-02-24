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
                movieIntroduc = ""
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

    #print(datalist)

    # print(t_list)

    return datalist

import xlwt

#3.保存解析数据到Excel
def savedata2Excel(savepath,datalist):
    print("saving...")
    book = xlwt.Workbook(encoding='utft-8',style_compression=0)     #创建表对象
    sheet = book.add_sheet("movieTop250")
    #定义表头
    col = ["电影详情链接","电影图片链接","电影中文名","电影外文名","电影简介","电影评分","参评人数","电影信息"]
    for i in range(len(col)):
        sheet.write(0,i,col[i])
    for i in range(len(datalist)):
        for j in range(len(col)):
            sheet.write(i+1,j,datalist[i][j])
    book.save(savepath)


import sqlite3
#4.保存源码数据到数据库sql
def saveData2Sql(dbpath,datalist):
    print("")
    init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()

    for data in datalist:
        for i in range(len(data)):
            if i == 5 or i ==6:
                continue
            else:
                data[i] = '"'+ data[i] + '"'
        # print(data)
        # data = ','.join(data)
        # print(data)
        sql = """
        insert into movie250 ( movie_link,pic_link,cname,ename,introduction,rated,judgeNum,movie_info
        ) values (%s);                
        """ %','.join(data)

        cursor.execute(sql)
        conn.commit()
    cursor.close()
    conn.close()




def init_db(dbpath):
    sql = """
         create table movie250
         (
         id integer primary key autoincrement,
         movie_link text,
         pic_link text,
         cname varchar,
         ename varchar,
         introduction text,
         rated numeric,
         judgeNum numeric,
         movie_info text
         );
    """
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()







if __name__ == '__main__':
    baseurl = "https://movie.douban.com/top250?start="
    # print(baseurl+str(2*25))
    #1. 获取网页源码并解析数据
    datalist = getDatalist(baseurl)

    #2. 保存数据到Excel
    # savepath = "豆瓣电影top250.xls"
    # savedata2Excel(savepath,datalist)

    #3. 保存数据到数据库sqlite
    dbpath = "movie.db"
    # init_db(dbpath)
    saveData2Sql(dbpath,datalist)
    print("爬取完成")