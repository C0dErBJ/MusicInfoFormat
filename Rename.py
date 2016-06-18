#-*- coding: UTF-8 -*-
#!/usr/bin/python
#批量格式化歌曲信息，通过酷狗搜索的接口获取歌曲信息
#todo 修改歌曲专辑图片
#todo 命令行

import eyed3
import os
import re
import urllib2
import urllib
import demjson
import shutil

musicPath = "/Users/C0dEr/Downloads/音乐/"
indexChar = '-'
isNeedRename = True
isNeedFixInfo = True


def FindMp3():
    if os.path.exists(musicPath) != True:
        print "未找到文件夹目录"
        return
    dir = os.listdir(musicPath)
    list = []
    for item in dir:
        fullpath = musicPath + item
        if (os.path.splitext(fullpath)[1].lower() == ".mp3".lower()):
            FixMp3Info(fullpath, Rename(fullpath, item))


def FixMp3Info(path, SN):
    if(len(SN) == 3):
        music = eyed3.load(SN[2])
        result = FindInfo(SN[1] + " - " + SN[0])
        if(result != None and len(result) == 3):
            music.initTag()
            music.tag.artist = unicode(result[0])
            music.tag.title = unicode(result[1])
            music.tag.album_artist = unicode(result[0])
            music.tag.album = unicode(result[2])
            music.tag.comment = u" "
            music.tag.save()
            if os.path.exists("Music") != True:
                os.makedirs("Music")
            shutil.move(path, os.path.abspath(os.curdir) + "/Music")

    else:
        print "不能找到" + path


def reset(music):
    # todo 重置音乐信息
    print "fd"


def FindInfo(keyword):
    url = u"http://ioscdn.kugou.com/api/v3/search/song?keyword="
    param = u"&page=1&pagesize=30&showtype=10&plat=2&version=8100&tag=1&correct=1&privilege=1&sver=5"
    response = urllib2.urlopen(
        (url + urllib.quote(keyword) + param))
    result = demjson.decode(response.read())
    print url + urllib.quote(keyword) + param
    if(len(result["data"]["info"]) > 0):
        return (result["data"]["info"][0]["singername"], result["data"]["info"][0]["songname"], result["data"]["info"][0]["album_name"])
    else:
        try:
            FindInfo(keyword.split('-')[1])
        except:
            return()


def test():
    url = "http://ioscdn.kugou.com/api/v3/search/song?keyword=Forever%20-%20Stratovarius&page=1&pagesize=30&showtype=10&plat=2&version=8100&tag=1&correct=1&privilege=1&sver=5"
    response = urllib2.urlopen(
        url)
    result = demjson.decode(response.read())
    if(result != None):
        return (result["data"]["info"][0]["singername"], result["data"]["info"][0]["songname"], result["data"]["info"][0]["album_name"])
    return ()


def Rename(path, item):
    name, extension = os.path.splitext(item)
    reg = "\\s*" + indexChar + "\\s*"
    pattern = re.compile(reg)
    matchs = pattern.split(name)
    if len(matchs) == 2:
        newname = musicPath + matchs[0] + " - " + matchs[1] + extension.lower()
        if(isNeedRename):
            os.rename(path, newname)
        return (matchs[0], matchs[1], newname)
    elif len(matchs) == 3:
        print item + "格式不正确,但已做调整，如果不正确请手动修改"
        newname = musicPath + matchs[0] + " - " + matchs[1] + extension.lower()
        if(isNeedRename):
            os.rename(path, newname)
        return (matchs[0], matchs[1], newname)
    else:
        print item + "格式不正确"
        return ()


if __name__ == "__main__":
    FindMp3()
