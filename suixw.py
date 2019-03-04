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
    '''���������ַ�'''
    str = str.replace('?','').replace('<','').replace('>','').replace('|','').replace(':','').replace('''"''','').replace('*','').replace('/','').replace('\\','')
    return str

text = '' #����ȫ�ֱ�����������Ӧ�ı�

def error(url):
    '''��������'''
    try:
        r = requests.get(url, headers=head, timeout=15)
    except:
        print('**' * 15 + '�������' + '**' * 15)
        time.sleep(1.5)
        error(url)
    else:
        time.sleep(2)
        r.encoding = 'gbk'
        global text #�޸�ȫ�ֱ���
        text = r.text

error(url)
r = etree.HTML(text)
nav_url_list = r.xpath("//ul[@class='navlist']/li/a/@href")[2:-3]
#�Ŀ�url�б�
nav_name_list = r.xpath("//ul[@class='navlist']/li/a/text()")[2:-3]
#�Ŀ������б�
for nav_url,nav_name in zip(nav_url_list,nav_name_list):
    if not os.path.exists('D:/������С˵/'+nav_name+''):
        os.makedirs('D:/������С˵/'+nav_name+'')
    error(nav_url)
    time.sleep(2)
    r = etree.HTML(text)
    page_list = set(r.xpath("//div[@class='pagelink']/a/@href")) #ҳ�������б�
    for page in page_list:
        page = url + page
        error(page)
        r = etree.HTML(text)
        novel_name_list = r.xpath("//div[@style='width:373px;float:left;margin:5px 0px 5px 5px;']/div/a/@title")
        #��С˵�����б�
        novel_url_list = r.xpath("//div[@style='width:373px;float:left;margin:5px 0px 5px 5px;']/div/a/@href")
        #��С˵url�б�
        for novel_url,novel_name in zip(novel_url_list,novel_name_list):
            novel_name = str_all_special(novel_name) #�����ַ������������������ַ�
            f = open('D:/������С˵/'+nav_name+'/'+novel_name+'.txt','a',encoding='utf-8')
            error(novel_url)
            r = etree.HTML(text)
            novel_introduce = r.xpath("//td[@width='80%' and @valign='top']//text()") #��С˵���
            for i in novel_introduce:
                print(i,file=f)
            chapter_url_list = r.xpath("//div[@style='text-align:center']/a/@href")[0]
            error(chapter_url_list)
            r = etree.HTML(text)
            chapter_url_list = r.xpath("//td[@class='ccss']/a/@href") #�½�url�б�
            chapter_name_list = r.xpath("//td[@class='ccss']/a/text()") #�½������б�
            for i,j in zip(chapter_url_list,chapter_name_list):
                if '��ͼ' not in j:
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