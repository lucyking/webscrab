#coding=utf-8
import urllib,urllib2
import  sys,os
from HTMLParser import HTMLParser
class MyParser(HTMLParser):
    resault='None'
    def __init__(self):
        HTMLParser.__init__(self)


    def get_pwd(self):
        return sys.path[0]


    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name, value in attrs:
                if name == 'href':
                    self.resault=value  # merge with latest apk
                    # print  value

    def getHtml(self,url):
        page = urllib.urlopen(url)
        html = page.read()
        # print  html
        return html


# if __name__ ==  ' __main__ ' :    <------ 该冒号为中文 导致run不会执行（直接拷贝网页代码的锅
if __name__ == '__main__':
    alpha  =  MyParser()
    html = alpha.getHtml('http://10.240.129.99/nightly/')
    # print html
    apk_list = alpha.feed(html)
    # print type(apk_list)
    print apk_list
    print alpha.resault
    apk_version = alpha.resault
    apk_version =apk_version.replace('/','')
    #alpha.feed(html)
    download_url = """http://10.240.129.99/nightly/"""+apk_version+'/'+apk_version+""".apk"""
    # print  download_url
    f = urllib2.urlopen(download_url)
    pwd = alpha.get_pwd()
    print pwd
    """
    data = f.read()
    filename= apk_version+".apk"
    with open(filename, "wb") as code:
        code.write(data)
    print "Download Done!"
    """

