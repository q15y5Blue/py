# coding:utf-8
# 分词
# from nltk.book import *
# from nltk.corpus import *
# import nltk
import jieba
import jieba.analyse as analyse


# 写文件
def importText(fileName = "content.txt", context=None):
    fl = open(fileName, 'a+')
    fl.write(context+"\n")
    fl.close()


# 读文本写文本readLines from tieba
def readLines():
    from crawBaidu.craw.dao.entity import reply
    repl = reply()
    size = repl.getNumbers()
    print(size)  # 3166511
    countSize = 300000; len = 5000
    for index in range(1, 61):
        if index * len > countSize: break
        reply_list = repl.getReply(sqlStr=None, count=(index*len, len))
        content_list = [reply_li[2] for reply_li in reply_list]
        importText("types", '^:^;'.join(content_list))

#
def readAsText():
    fl = open('types', 'r').read()
    str_list = fl.split("^:^;")
    for i in range(len(str_list)):
        print(str_list[i])

# jieba 读
def readText():
    fl = open("types", 'r').read()
    jieba.load_userdict("./data/keyWords")
    jieba.analyse.set_stop_words("./data/stopWords")
    fl = open('types', 'r').read()
    str_list = fl.split("^:^;")
    for i in range(len(str_list)):
        seg_list = jieba.cut(str(str_list[i]))
        print("  ".join(seg_list))
    # tags = jieba.analyse.extract_tags(fl, topK=100, withWeight=True)  # IDF 分词
    # for tag in tags:
    #     print("tag: %s\t\t weight: %f" % (tag[0], tag[1]))


if __name__ == '__main__':
    # readLines()
    readText()
