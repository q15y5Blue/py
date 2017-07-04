#coding:utf8
#class类 并且还有类似Java的一些set get方法
from datetime import datetime
class News(object):
    @property
    def id(self):
        return self.id
    
    @id.setter
    def id(self,value):
        if not isinstance(value,int):
            raise ValueError("必须是int类型的id")
        self._value=value
    
    #新闻内容
    @property
    def content(self):
        return self._content
    
    @content.setter
    def content(self, value):
        if not isinstance(value, str):
            raise ValueError('type must be an str!')
        self._content = value
    
    #新闻作者
    @property
    def authors(self):
        return self._authors
    
    @authors.setter
    def authors(self, value):
        if not isinstance(value, str):
            raise ValueError("type must be str~")
        self._authers = value
    
    #新闻url
    @property
    def url(self):
        return self._url
    
    @url.setter
    def url(self, value):
        if not isinstance(value, str):
            raise ValueError("type must be str~")
        self._url = value
    
    #新闻来源
    @property
    def src(self):
        return self._src
    
    @src.setter
    def src(self, value):
        if not isinstance(value, str):
            raise ValueError("type must be str~")
        self._src = value
    
    #新闻发布时间
    @property
    def tim(self):
        return self._tim
    
    #时间
    @tim.setter
    def tim(self,value):
        if not isinstance(value,datetime):
            raise ValueError("type must be float~!")
        self._tim = value
