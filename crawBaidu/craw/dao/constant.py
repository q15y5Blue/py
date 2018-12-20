#coding:utf-8


class NameList(object):
    def __init__(self, maxSize=50):
        self.list = []
        self.maxSize = maxSize
        self.count = 0

    def addList(self,obj):
        if self.list.__len__() < self.maxSize and self.existsObj(obj) is not True:
            self.list.append(obj)
        elif self.existsObj(obj) is not True:
            self.list.pop(0)
            self.list.append(obj)

    def existsObj(self,obj):
        return obj in self.list
#
# if __name__=='__main__':
#     nameList = NameList(20)
#     for i in range(0, 50):
#         nameList.addList(i)
#         print(nameList.list)
#         print(nameList.existsObj(20))