#class类 并且还有一些set get方法
class News(object):
    @property
    def content(self):
        return self._content
    
    @content.setter
    def content(self, value):
        if not isinstance(value, str):
            raise ValueError('type must be an str!')
        self._content = value
    
    @property
    def author(self):
        return self._author
    
    @author.setter
    def author(self, value):
        if not isinstance(value, str):
            raise ValueError("type must be str~")
        self._auther = value
    
    @property
    def url(self):
        return self._url
    
    @url.setter
    def url(self, value):
        if not isinstance(value, str):
            raise ValueError("type must be str~")
        self._url = value
    
    @property
    def src(self):
        return self._src
    
    @src.setter
    def src(self, value):
        if not isinstance(value, str):
            raise ValueError("type must be str~")
        self._src = value
    
