#coding:utf8
#class类 并且还有类似Java的一些set get方法
class News(object):
    
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
    def author(self):
        return self._author
    
    @author.setter
    def author(self, value):
        if not isinstance(value, str):
            raise ValueError("type must be str~")
        self._auther = value
    
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
    #property
    def time(self):
        return self._time
    
    @time.setter
    def time(self,value):
        if not isinstance(value,str):
            raise ValueError("type must be str~!")
        self._time = value