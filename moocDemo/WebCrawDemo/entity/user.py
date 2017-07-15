'''
Created on 2017年7月13日
user
@author: q15y5Blue
'''
class user(object):
    @property
    def user_id(self):
        return self._user_id
    
    @user_id.setter
    def user_id(self,value):
        if not isinstance(value, int):
            raise ValueError("not int ")
        self.user_id=value
        
    @property
    def avatar(self):
        return self._avatar
    
    @avatar.setter
    def avatar(self,value):
        if not isinstance(value, str):
            raise ValueError("not str")
        self._avatar=value
        
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self,value):
        if not isinstance(value, int):
            raise ValueError("not int ")
        self.id=value
        
    @property
    def location(self):
        return self._location
    
    @location.setter
    def location(self,value):
        if not isinstance(value, str):
            raise ValueError("not str")
        self._location=value
        
    @property 
    def nickname(self):
        return self._nickname
    
    @nickname.setter
    def nickname(self,value):
        if not isinstance(value, str):
            raise ValueError("not str")
        self._nickname=value
        
    @property
    def redNameInfo(self):
        return self._redNameInfo
    
    @redNameInfo.setter
    def redNameInfo(self,value):
        if not isinstance(value, object):
            raise ValueError("this is not a obj")
        self._redNameInfo=value
        
    @property
    def userId(self):
        return self._userId
    
    @userId.setter
    def userId(self,value):
        if not isinstance(value, int):
            raise ValueError("not int")
        self._userId=value
        
    @property
    def vipInfo(self):
        return self._vipInfo
    
    @vipInfo.setter
    def vipInfo(self,value):
        if not isinstance(value, str):
            raise ValueError("not str")
        self._vipInfo=value