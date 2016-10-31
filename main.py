#-*- coding: utf-8 -*-
import os
import re
import sys, urllib, urllib2
import time
import cookielib

class Github(object):
    # 初始化
    def __init__(self,name,password):
        self.user = name
        self.password = password
        self.cookie = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        urllib2.install_opener(self.opener)
        getCookieUrl = "https://github.com/login"
        self.html = urllib2.urlopen(getCookieUrl).read()

    # 模拟浏览器行为，得到Cookie
    def _getHeaders(self,referer):
        headers = {}
        headers['User-Agent']='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        headers['Connection']='keep-alive'
        headers['Cache-Control']='max-age=0'
        headers['Accept-Language']='zh-CN,zh;q=0.8,en;q=0.6'
        headers['Accept']='text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        headers['Referer']= referer
        return headers
    # 方法登录网站
    def login(self):
        print "正在获取获取authenticity_token"
        token = self.getUserToken(self.html)[0]
        loginparams = {
        'commit' : 'Sign in',
        'utf8' : '%E2%9C%93',
        'authenticity_token' : token,
        'login' : self.user,
        'password' : self.password
        }
        #post数据登录
        req = urllib2.Request( 'https://github.com/session', urllib.urlencode(loginparams), headers=self._getHeaders('https://github.com/login'))
        resp = urllib2.urlopen(req)
        self.operate = self.opener.open(req)
        thePage = resp.read().decode("utf-8")
        #查看登录结果
        print token
        print "登陆成功"
        return thePage
    # 获取Token
    def getUserToken(self,part):
        reg = re.compile('authenticity_token".*?value="(.*?)".*?>');
        result = re.findall(reg,part)
        return result
    def getUserList(self,part):
        reg = re.compile('link-gray.*?pl-1.*?>(.*?)</span>');
        result = re.findall(reg,part)
        return result
    def followUser(self,token,username):
        loginparams = {
        'utf8' : '%E2%9C%93',
        'authenticity_token' : token
        }
        #post数据登录
        req = urllib2.Request( 'https://github.com/users/follow?target='+username, urllib.urlencode(loginparams), headers=self._getHeaders(''))
        resp = urllib2.urlopen(req)
        self.operate = self.opener.open(req)
        thePage = resp.read().decode("utf-8")
        return thePage

    # 获取复制用户的用户列表
    def listFollow(self,page,copyusername):
        url = "http://github.com/" + copyusername + "?page="+ str(page) +"&tab=following"
        req = urllib2.Request(url,headers=self._getHeaders(''))
        response = urllib2.urlopen(req)
        self.opener.open(req)
        thePage = response.read()
        tokenlist = self.getUserToken(thePage)
        userlist = self.getUserList(thePage)
        for i in range(len(userlist)):
            time.sleep(1)
            print "正在第"+ str(page) +"页关注：" + userlist[i] + " Token：" + tokenlist[i]
            self.followUser(tokenlist[i],userlist[i])

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

#自动关注~ 用户名 密码
gt = Github('username','password')
# 登录
gt.login()
# range内是页数
for i in range(1,5):
    gt.listFollow(i,'yfgeek') #复制列表的人
print "结束啦"
