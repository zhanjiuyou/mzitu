# 2020年8月27日
# 本次爬虫主要任务是爬取妹子图网站的图片，此代码只用于python技术的研究探讨，不做其他用途。
# 郑重申明：切勿用于非法用途，后果自负。由于此网站图片尺度较大，读者只需关注本代码研究代码本身，切勿关注其内容，切勿非法传播。如有问题请及时联系我反馈谢谢。
# 个人博客：https://jiaokangyang.com

import requests
import threading
from pyquery import PyQuery as py
import time
import os


# 这里我们先创建一个字典，将对应目录的缩写设置好便于后面调用，随便写了几个，要想更多自行添加
mulu = {
    '日本':'japan',
    '台湾':'taiwan',
    '清纯':'mm',
    '性感':'xinggan',
    '最热':'hot'
}
s = input('请输入你要爬取的分类名称\n目前有以下分类可供爬取：日本、台湾、清纯、性感、最热。\n')
if s not in mulu:
    s = input('输入内容不在爬取范围请重新输入：')



# 创建函数爬取页面源码并输出
def down_page(url):
    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3775.400 QQBrowser/10.6.4208.400',
    }
    r = requests.get(url,headers=headers)
    return r.text

# 获取每个套图的页面列表，并下载文件
def get_pic_list(html):
    pics = py(html)
    taotu_lists = pics('#pins li ').items() # 将获取到的内容
    for list in taotu_lists:
        link = list('a').attr('href')
        text = list('span a').text()
        get_pic(link,text)

# 获取每个套图中的前十个图片
def get_pic(link,text):    #  这里传递两个参数，一是获取图片，二是将获取到的图片放到对应的文件夹下面

    for i in range(1,11):    # 由于此网站每个套图页面只有一张图片，而且数量较多，所以我们默认抓取前10张
        # 这块将每个图片的页码加到后面组成新的链接
        url = link + '/' + str(i)
        html = down_page(url)  # 用我们写得第一个函数获取获取网页的源码
        pic = py(html)
        pic_link = pic('.main-image p a img ').attr('src')
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3775.400 QQBrowser/10.6.4208.400',
            'referer':'https://www.mzitu.com',
        }
        create_dir('pic/{}'.format(text)) # 创建套图的文件夹
        r = requests.get(pic_link,headers=headers)
        with open('pic/{}/{}'.format(text,str(i)+'.jpg'),'wb') as f:
            f.write(r.content)
            time.sleep(1)


# 在系统桌面创建目录
def create_dir(name):
    if not os.path.exists(name):
        os.makedirs(name)

# 为了便于后边多线程的调用，这里将执行的操作进行函数封装
def execute(url):
    html = down_page(url)
    get_pic_list(html)

# 主函数，整体程序运行
def main():
    create_dir('pic')
    pages = [i for i in range(1,20)]   # 将前5页的页码写到列表里面，如需获取更多自行更改
    threads = []  # 构建多线程池子，控制在5个线程内
    while len(pages)>0: # 确定有页面可爬
        for thread in threads:
            if not thread.is_alive(): #判断线程是否运行，没有运行则从列表中移除
                threads.remove(thread)

        while len(threads)<5 and len(pages)>0: #最大线程控制在5个
            cur_page = pages.pop(0)    # 正常运行的话，先从发页面列表中吧第一个移除掉
            url =  'https://www.mzitu.com/{}/page/{}'.format(mulu[s],cur_page)
            print(url)
            thread = threading.Thread(target=execute,args=(url,)) # 多线程运行execute函数
            thread.start()  # 启动多线程
            print('同时正在下载{}页'.format(cur_page))
            threads.append(thread)


if __name__ == '__main__':
    main()

