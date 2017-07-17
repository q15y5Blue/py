'''
Created on 2017年7月13日

@author: q15y5Blue
'''
from datetime import datetime

class Reply(object):
    
    @property
    def reply_ids(self):
        return self._reply_ids
    
    @reply_ids.setter
    def reply_ids(self,value):
        if not isinstance(value,int):
            raise ValueError("intintintintint!")
        self._reply_ids=value
        
    @property
    def against(self):
        return self._against
    
    @against.setter
    def against(self,value):
        if not isinstance(value,int):
            raise ValueError("intintintintint!")
        self._against=value
    
    @property
    def anonymous(self):     
        return self._anonymous
    
    @anonymous.setter
    def anonymous(self,value):
        if not isinstance(value,bool):
            raise ValueError("not bool")
        self._anonymous=value
    
    @property
    def buildlevel(self):
        return self._buildlevel
    
    @buildlevel.setter
    def buildlevel(self,value):
        if not isinstance(value, int):
            raise ValueError("not int")
        self._buildlevel=value
        
    @property
    def commentId(self):
        return self._commentId
    
    @commentId.setter
    def commentId(self,value):
        if not isinstance(value, int):
            raise ValueError("not str")
        self._commentId=value
        
    @property
    def content(self):
        return self._content
    
    @content.setter
    def content(self,value):
        if not isinstance(value, str):
            raise ValueError("not str")
        self._content=value
        
    @property
    def creatTime(self):
        return self._creatTime
    
    @creatTime.setter
    def creatTime(self,value):
        if not isinstance(value, str):
            raise ValueError("not datetime type!~")
        self._creatTime=value
        
    @property
    def favCount(self):
        return self._favCount
    
    @favCount.setter
    def favCount(self,value):
        if not isinstance(value, int):
            raise ValueError("not int~!")
        self._favCount=value
        
    @property
    def ip(self):
        return self._ip
    
    @ip.setter
    def ip(self,value):
        if not isinstance(value,str):
            raise ValueError("not str~!")
        self._ip=value
        
    @property
    def idDel(self):
        return self._idDel
    
    @idDel.setter
    def idDel(self,value):
        if not isinstance(value, bool):
            raise ValueError("not bool")
        self._idDel=value
        
    @property
    def postId(self):
        return self._postId
    
    @postId.setter
    def postId(self,value):
        if not isinstance(value, str):
            raise ValueError("not str")
        self._postId=value
        
    @property
    def productKey(self):
        return self._productKey
    
    @productKey.setter
    def productKey(self,value):
        if not isinstance(value, str):
            raise ValueError("not str")
        self._productKey=value
        
    @property
    def shareCount(self):    
        return self._shareCount
    
    @shareCount.setter
    def shareCount(self,value):
        if not isinstance(value, int):
            raise ValueError("not int ")
        self._shareCount=value
        
    @property
    def siteName(self):
        return self._siteName
    
    @siteName.setter
    def siteName(self,value):
        if not isinstance(value, str):
            raise ValueError("not str")
        self._siteName=value
        
    @property
    def source(self):
        return self._source
    
    @source.setter
    def source(self,value):
        if not isinstance(value, str):
            raise ValueError("not str")
        self._source=value
        
    @property
    def unionState(self):
        return self._unionState
    
    @unionState.setter
    def unionState(self,value):
        if not isinstance(value, bool):
            raise ValueError("not bool")
        self._unionState=value
        
    @property
    def vote(self):
        return self._vote
    
    @vote.setter
    def vote(self,value):
        if not isinstance(value, int):
            raise ValueError("not int")
        self._vote=value
        
    
    
    
    
