# coding=utf-8
import urllib, urllib2
import sys, os,threading
from time import ctime,sleep
from HTMLParser import HTMLParser


class MyParser(HTMLParser):
    resault = 'None'
    pwd = "/your/script/init/path"

    def __init__(self):
        HTMLParser.__init__(self)

    def get_pwd(self):
        return sys.path[0]

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name, value in attrs:
                if name == 'href':
                    self.resault = value  # merge with latest apk
                    # print  value

    def getHtml(self, url):
        page = urllib.urlopen(url)
        html = page.read()
        # print  html
        return html

    def startAppium(self):
        cmd = 'start /b appium'
        # cmd = 'date'
        # print "[%s]:" %ctime()
        print "-------%s-------" %ctime()
        print os.popen(cmd).read()

    def job_1(self):
        html = self.getHtml('http://10.240.129.99/nightly/')
        apk_list = self.feed(html)
        print "-------%s-------" %ctime()
        print apk_list
        print self.resault
        apk_version = self.resault
        apk_version = apk_version.replace('/','')
        download_url = """http://10.240.129.99/nightly/""" + apk_version + '/' + apk_version + """.apk"""
        f = urllib2.urlopen(download_url)
        self.pwd = self.get_pwd()
        print self.pwd

        data = f.read()
        filename= apk_version+".apk"
        with open(filename, "wb") as code:
            code.write(data)
        print "Download Done!"

        cmd = """pybot --variable BROWSER:safari --outputdir safari_dir --include demo --xunit output_xunit.xml --xunitskipnoncritical Test/YX_Subscriptions/test_suite_examples.txt"""
        # print "[%s]:" %ctime()
        print "-------%s-------" %ctime()
        print os.popen(cmd).read()






# if __name__ ==  ' __main__ ' :    <------ 该冒号为中文 导致run不会执行
if __name__ == '__main__':

    MyParser = MyParser()
    """
    html = MyParser.getHtml('http://10.240.129.99/nightly/')
    # print html
    apk_list = MyParser.feed(html)
    # print type(apk_list)
    print apk_list
    print MyParser.resault
    apk_version = MyParser.resault
    apk_version = apk_version.replace('/', '')
    # MyParser.feed(html)
    download_url = "http://10.240.129.99/nightly/" + apk_version + '/' + apk_version + ".apk"
    # print  download_url
    f = urllib2.urlopen(download_url)
    MyParser.pwd = MyParser.get_pwd()
    print MyParser.pwd

    # cmd = "pybot --variable BROWSER:safari --outputdir safari_dir --include demo --xunit output_xunit.xml --xunitskipnoncritical Test/YX_Subscriptions/test_suite_examples.txt"
    # print os.popen(cmd).read()


    data = f.read()
    filename= apk_version+".apk"
    with open(filename, "wb") as code:
        code.write(data)
    print "Download Done!"

    MyParser.startAppium()
    """
    threads = []
    t1 = threading.Thread(target=MyParser.startAppium())
    t2 = threading.Thread(target=MyParser.job_1())
    threads.append(t1)
    threads.append(t2)
    for t in threads:
        t.start()
    for t in threads:
        t.join()





