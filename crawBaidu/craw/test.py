# coding:utf-8
def test(strs=None, count=None):
    print(count)
    if strs is  None:
        strs = "strsss %s " % count
        print(str)
    strs = strs % count
    print(strs)


if __name__ =='__main__':
    count = (100, 1100)
    print(count[1])
    # print("asdasd %s "%(100))