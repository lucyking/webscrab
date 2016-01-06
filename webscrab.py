# coding=utf-8
import urllib, urllib2
import sys, os, re, getopt
import threading, platform, subprocess
from time import ctime, sleep
from HTMLParser import HTMLParser


class MyParser(HTMLParser):
    xunit = 'NULL'
    version = 'NULL'
    include = 'NULL'
    testcase = 'NULL'
    outputdir= 'NULL'
    input_cmd =''

    dev_model = 'NULL'
    dev_os_version = 'NULL'
    dev_manufacturer = 'NULL'

    resault = 'NULL'
    pwd = "/your/script/workspace/path"

    def __init__(self):
        HTMLParser.__init__(self)

    def usage(self):
        print "user instroduction ;-)"

    def get_version(self):
        print "version 1.0.0"

    def get_pwd(self):
        return sys.path[0]

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name, value in attrs:
                if name == 'href':
                    self.resault = value  # merged by the latest version info

    def getHtml(self, url):
        page = urllib.urlopen(url)
        html = page.read()
        return html

    def startAppium(self):
        # cmd = 'start /b appium'
        # cmd = 'nohup appium & '
        # cmd = 'echo `nohup /usr/local/bin/appium &` &'
        cmd = 'ps aux'
        print "-------%s-------" % ctime()
        print os.popen(cmd).read()

    def create_output_dir(self):
        if os.path.exists('./RFUI_outputs_dir'):
            print ">>>RFUI_outputs_dir already exists"
        else:
            cmd = "mkdir RFUI_outputs_dir"
            print '>>>' + os.popen(cmd).read()

    def get_newest_apk(self):
        html = self.getHtml('http://10.240.129.99/nightly/')
        self.feed(html)  # -->def handle_starttag():
        print "-------%s-------" % ctime()
        apk_version = self.resault
        apk_version = apk_version.replace('/', '')

        fl = open('test_dev_info.properties', 'a')
        fl.write('android_app_version=' + apk_version + '\n')
        fl.close()

        if os.path.exists('./' + apk_version + '.apk'):
            print "the Apk already up-to-date\n"
            sleep(8)  # wait appium start
        else:
            download_url = "http://10.240.129.99/nightly/" + apk_version + '/' + apk_version + ".apk"
            f = urllib2.urlopen(download_url)
            self.pwd = self.get_pwd()
            print self.pwd
            data = f.read()
            filename = apk_version + ".apk"
            with open(filename, "wb") as code:  # download newest apk
                code.write(data)
            print "Download Done!"
            sleep(8)  # wait appium start

        # rm the old apk
        # cmd = "rm ./YX_RFUI_Framework_demo/Resources/yixin_test.apk"
        # print os.popen(cmd).read()

        # link newest apk to ./Res*/yixin_test.apk
        # Win:ln <src>  <des>  |  Mac/Linux: ln -s <src> <des>
        uname_str = platform.system()
        os_arch = re.search("Windows", uname_str)
        if os_arch:
            cmd = "copy /y  .\\" + apk_version + ".apk" + "  .\\Resources\\yixin_test.apk"
            print os.popen(cmd).read()
        else:
            cmd = "ln -s ./" + apk_version + ".apk" + "   ./Resources/yixin_test.apk"
            print os.popen(cmd).read()

    def get_device_info(self):
        cmd = "adb shell cat /system/build.prop"
        dev_info = os.popen(cmd).read()
        if dev_info:
            self.dev_manufacturer = re.search(r"(ro.product.manufacturer=)(\S+)", dev_info).group(2)
            self.dev_model = re.search(r"(ro.product.model=)(\S+)", dev_info).group(2)
            self.dev_os_version = re.search(r"(ro.build.version.release=)(\S+)", dev_info).group(2)
            print '>>>' + self.resault.replace('/', '')
            print '>>>' + self.dev_manufacturer, self.dev_model, self.dev_os_version
            fl = open('test_dev_info.properties', 'a')
            fl.write('android_dev_name=' + self.dev_manufacturer + '\n')
            fl.write('android_dev_model=' + self.dev_model + '\n')
            fl.write('android_version=' + self.dev_os_version + '\n')
            fl.close()
        else:
            print ">>>No device find!"

    def get_gitbucket(self):
        cmd = "git clone https://git.hz.netease.com/git/yxplusQA/YX_RFUI_Framework_demo.git"
        print os.popen(cmd).read()

    def job_Mac(self):
        print "\n\n>>>here is from Mac\n\n"
        cmd = ' '.join(self.input_cmd)
        cmd = 'pybot'+' '+cmd
        print os.popen(cmd).read()

    def job_Windows(self):
        print "\n\n>>>here is from Windows\n\n"
        cmd = ' '.join(self.input_cmd)
        cmd = 'C:\Python27\python -m robot.run'+' '+cmd
        print os.popen(cmd).read()

    def job_Linux(self):
        print "[info]:Linux fx() need added in future ;-)"

    def job_operate(self):
        uname_str = platform.system()
        if re.search("Darwin", uname_str):
            self.job_Mac()
        elif re.search("Windows", uname_str):
            self.job_Windows()
        elif re.search("Linux", uname_str):
            self.job_Linux()
        else:
            print "[x]:can NOT detect OS type :-("



if __name__ == '__main__':
    
    MyParser = MyParser()
    MyParser.input_cmd = sys.argv[1:]

    MyParser.create_output_dir()  # mkdir ./RFUI_outputs_dir
    MyParser.get_newest_apk()  # wget http://10.240.129.99/nightly/*_latest.apk
    MyParser.get_device_info()  # adb shell cat /system/build.prop
    # MyParser.get_gitbucket()  # git clone *_demo
    MyParser.job_operate()
"""
    uname_str = platform.system()
    print uname_str
    mac_arch = re.search("Darwin", uname_str)
    win_arch = re.search("Windows", uname_str)
    linux_arch = re.search("Linux", uname_str)

    if mac_arch:
        MyParser.job_Mac()
    elif win_arch:
        MyParser.job_Windows()
    elif linux_arch:
        MyParser.job_Linux()
    else:
        print "[x]:can NOT detect OS type :-("
"""