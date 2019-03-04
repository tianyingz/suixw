# coding=gbk
import requests,time,os
from lxml import etree

url = 'http://book.suixw.com'
head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
        "Host": "book.suixw.com",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9"}

def str_all_special(str):
    '''处理特殊字符'''
    str = str.replace('?','').replace('<','').replace('>','').replace('|','').replace(':','').replace('''"''','').replace('*','').replace('/','').replace('\\','')
    return str

text = '' #定义全局变量，接收响应文本

def error(url):
    '''处理请求'''
    try:
        r = requests.get(url, headers=head, timeout=15)
    except:
        print('**' * 15 + '请求出错' + '**' * 15)
        time.sleep(1.5)
        error(url)
    else:
        time.sleep(2)
        r.encoding = 'gbk'
        global text #修改全局变量
        text = r.text

error(url)
r = etree.HTML(text)
nav_url_list = r.xpath("//ul[@class='navlist']/li/a/@href")[2:-3]
#文库url列表
nav_name_list = r.xpath("//ul[@class='navlist']/li/a/text()")[2:-3]
#文库名称列表
for nav_url,nav_name in zip(nav_url_list,nav_name_list):
    if not os.path.exists('D:/随想轻小说/'+nav_name+''):
        os.makedirs('D:/随想轻小说/'+nav_name+'')
    error(nav_url)
    time.sleep(2)
    r = etree.HTML(text)
    page_list = set(r.xpath("//div[@class='pagelink']/a/@href")) #页面链接列表
    for page in page_list:
        page = url + page
        error(page)
        r = etree.HTML(text)
        novel_name_list = r.xpath("//div[@style='width:373px;float:left;margin:5px 0px 5px 5px;']/div/a/@title")
        #轻小说名称列表
        novel_url_list = r.xpath("//div[@style='width:373px;float:left;margin:5px 0px 5px 5px;']/div/a/@href")
        #轻小说url列表
        for novel_url,novel_name in zip(novel_url_list,novel_name_list):
            novel_name = str_all_special(novel_name) #调用字符处理函数，处理特殊字符
            f = open('D:/随想轻小说/'+nav_name+'/'+novel_name+'.txt','a',encoding='utf-8')
            error(novel_url)
            r = etree.HTML(text)
            novel_introduce = r.xpath("//td[@width='80%' and @valign='top']//text()") #轻小说简介
            for i in novel_introduce:
                print(i,file=f)
            chapter_url_list = r.xpath("//div[@style='text-align:center']/a/@href")[0]
            error(chapter_url_list)
            r = etree.HTML(text)
            chapter_url_list = r.xpath("//td[@class='ccss']/a/@href") #章节url列表
            chapter_name_list = r.xpath("//td[@class='ccss']/a/text()") #章节名称列表
            for i,j in zip(chapter_url_list,chapter_name_list):
                if '插图' not in j:
                    error(i)
                    r = etree.HTML(text)
                    chapter_name = r.xpath("//div[@id='title']/text()")
                    chapter_content = r.xpath("//div[@id='content']//text()")
                    for i in chapter_name:
                        print(i,file=f)
                    for j in chapter_content:
                        print(j,file=f)
                    print(nav_name,novel_name,i)
                    time.sleep(3)