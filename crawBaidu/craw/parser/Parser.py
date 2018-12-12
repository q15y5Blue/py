# coding:utf-8
import re

from bs4 import BeautifulSoup
from crawBaidu.craw.download.DownLoader import Downloader
from crawBaidu.craw.dao.entity import *
from crawBaidu.craw.parser import *
from crawBaidu.craw.dao.proxy import Proxies
import time
import json

class Parser:
    # 公用解析方法,使用BeautifulSoup模块
    def parse_url(self, url, info=None):
        dt = Downloader()
        req = dt.reqGet(url, proxy=Proxies(db='cn'))
        if req.status_code == 200:
            jsonData = req.json().get('data')
            if info is None:
                if jsonData.get('html'):
                    jsonData = jsonData.get['html']
                elif jsonData.get('content'):
                    jsonData = jsonData['content']
                soup = BeautifulSoup(jsonData, "html.parser")
                return soup
            else:
                return jsonData

    #parser ArticleList
    def parserArticleList(self, url):
        soup = self.parse_url(url)
        list = soup.find_all('li', class_='tl_shadow tl_shadow_new')
        for result in list:
            ar = article()
            ar.title = result.find('div', class_='ti_title').text.strip()
            ar.date = getTime(result.find('span', class_='ti_time').text.strip())
            ar.id = result.find('a', class_='j_common ti_item')['tid'].strip()
            ar.username = result.find('span', class_='ti_author').text.strip()
            ar.user.img_path = result.find('img')['src']
            ar.user.username = result.find('span', class_='ti_author').text.strip()
            if ar.checkArticleExists() is None:
                ar.replyList = self.crawReplyExecute(ar)
                ar.importArticle()

    def crawReplyExecute(self, article):
        url = "https://tieba.baidu.com/mo/q/m?kz=%s&is_ajax=1&post_type=normal&_t=%d&pn=%s&is_ajax=1"
        articleInfoUrl = url % (article.id, int(time.time()), str(0))
        infoJson = self.parse_url(articleInfoUrl, info=1)
        pageInfo = infoJson.get('page'); totalPage = pageInfo.get('total_page'); offSet = pageInfo.get("page_size")
        rsList = []
        for nowPage in range(1, totalPage + 1):
            if nowPage == 1:
                doct = infoJson.get('html')
                list = self.parseReplyDetails(articleObj=article, doc=doct)
                # rsList.extend(list)
            else:
                articleMoreInfoUrl = url % (
                article.id, int(time.time()), str(offSet * nowPage))  # articleId time pn
                infoJson = self.parse_url(articleMoreInfoUrl, info=1)
                list = self.parseReplyDetails(articleObj=article, doc=infoJson.get("html"))
                # rsList.extend(list)
        return rsList

    def parseReplyDetails(self,articleObj=None,doc=None):
        soup = BeautifulSoup(doc, "html.parser")
        list = soup.find_all('li', class_='list_item')
        replyList = []
        childRsList = []  # 回复的回复，child of reply
        for li in list:
            rp = reply()
            userinf = li['data-info']
            userinfo = json.loads(userinf)
            rp.author = userinfo['un']
            rp.id = userinfo['pid']
            rp.floor_num = userinfo['floor_num']
            rp.content = li.find('div', class_='content').text.strip()
            if rp.floor_num == 1 and articleObj.content == '':
                articleObj.content = rp.content
            rp.date = getTime(li.find('span', class_='list_item_time').text.strip())
            rp.user.username = li.find('span', class_="user_name").text.strip()
            rp.user.img_path = str(li.find('img', class_="user_img")['src']).replace("amp;", "")
            childList = li.find('ul', class_='flist')  # 有flist属性才会有回复
            if childList is not None:
                if li.find('a', class_='fload_more_btn') is not None:
                    continue
                else:
                    for child in childList:
                        if type(child).__name__ == 'Tag':
                            chi = reply()
                            usinf = child['data-info']
                            usinfo = json.loads(usinf)
                            chi.author = usinfo['un']
                            chi.id = usinfo['pid']
                            chi.fn = rp.id
                            chi.user.username = chi.author
                            childRsList.append(chi)
            replyList.append(rp)
        replyList.extend(childRsList)
        return replyList


if __name__ == '__main__':
    par = Parser()
    url ="https://tieba.baidu.com/mo/q/m?kw=剑网3&pn=%d&lm=0&cid=0&has_url_param=0&is_ajax=1"
    par.parserArticleList(url)
