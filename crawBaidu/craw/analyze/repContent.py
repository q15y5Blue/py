# coding:utf-8
# 分词
import jieba
import jieba.analyse as analyse


# 写文件
def importText(fileName = "content.txt", context=None):
    fl = open(fileName, 'a+')
    fl.write(context+"\n")
    fl.close()

# 读文本写文本
def readLines():
    from crawBaidu.craw.dao.entity import reply
    repl = reply()
    size = repl.getNumbers()
    print(size)  # 3166511
    countSize = 300000; len = 1000
    for index in range(1, 301):
        if index * len > countSize: break
        reply_list = repl.getReply(sqlStr=None, count=(index*len, len))
        content_list = [reply_li[2] for reply_li in reply_list]
        importText("types", ' '.join(content_list) )


def readText():
    fl = open("content.txt", 'r').read()
    jieba.load_userdict("./data/keyWords")
    jieba.analyse.set_stop_words("./data/stopWords")
    tags = jieba.analyse.extract_tags(fl, topK=100)  # IDF 分词
    print(",".join(tags))

if __name__ == '__main__':
    readLines()
    # readText()
