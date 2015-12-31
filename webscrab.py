# coding=utf-8
import urllib, urllib2
import sys, os,re, threading,platform,subprocess
from time import ctime, sleep
from HTMLParser import HTMLParser


class MyParser(HTMLParser):
    resault = 'None'
    pwd = "/your/script/init/path"
    dev_manufacturer = 'None'
    dev_model = 'None'
    dev_os_version = 'None'

    def __init__(self):
        HTMLParser.__init__(self)

    def get_pwd(self):
        return sys.path[0]

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name, value in attrs:
                if name == 'href':
                    self.resault = value  # merge with the latest apk

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
        if  os.path.exists('./RFUI_outputs_dir'):
            print ">>>RFUI_outputs_dir already exists"
        else:
            cmd = "mkdir RFUI_outputs_dir"
            print '>>>'+os.popen(cmd).read()

    def get_newest_apk(self):
        html = self.getHtml('http://10.240.129.99/nightly/')
        apk_list = self.feed(html)
        print "-------%s-------" % ctime()
        print apk_list
        print self.resault
        apk_version = self.resault
        apk_version = apk_version.replace('/', '')
        print apk_version

        fl=open('test_dev_info.properties','a')
        fl.write('android_app_version='+apk_version+'\n')
        fl.close()

        if  os.path.exists('./'+apk_version+'.apk'):
            print "the Apk already up-to-date\n"
            sleep(8) # wait appium start
        else:
            download_url = "http://10.240.129.99/nightly/" + apk_version + '/' + apk_version + ".apk"
            f = urllib2.urlopen(download_url)
            self.pwd = self.get_pwd()
            print self.pwd
            data = f.read()
            filename = apk_version + ".apk"
            with open(filename, "wb") as code: #download newest apk
                code.write(data)
            print "Download Done!"
            sleep(8) # wait appium start

        # rm the old apk
        cmd = "rm ./YX_RFUI_Framework_demo/Resources/yixin_test.apk"
        print os.popen(cmd).read()

        # link newest apk to ./Res*/yixin_test.apk
        # Win:ln <src>  <des>  |  Mac/Linux: ln -s <src> <des>
        uname_str = platform.system()
        os_arch =  re.search("Windows",uname_str)
        if os_arch:
            cmd = "ln  ./"    + apk_version + ".apk" + "   ./YX_RFUI_Framework_demo/Resources/yixin_test.apk"
            print os.popen(cmd).read()
        else:
            cmd = "ln -s ./" + apk_version + ".apk" + "   ./YX_RFUI_Framework_demo/Resources/yixin_test.apk"
            print os.popen(cmd).read()


    def get_device_info(self):
        cmd = "adb.exe shell cat /system/build.prop"
        dev_info = os.popen(cmd).read()
        if dev_info:
            self.dev_manufacturer = re.search(r"(ro.product.manufacturer=)(\S+)",dev_info).group(2)
            self.dev_model = re.search(r"(ro.product.model=)(\S+)",dev_info).group(2)
            self.dev_os_version= re.search(r"(ro.build.version.release=)(\S+)",dev_info).group(2)
            print '>>>'+self.resault
            print '>>>'+self.dev_manufacturer,self.dev_model,self.dev_os_version
            fl=open('test_dev_info.properties','a')
            fl.write('android_dev_name='+self.dev_manufacturer+'\n')
            fl.write('android_dev_model='+self.dev_model+'\n')
            fl.write('android_version='+self.dev_os_version+'\n')
            fl.close()
        else:
            print ">>>No device find!"

    def get_gitbucket(self):
        cmd = "git clone https://git.hz.netease.com/git/yxplusQA/YX_RFUI_Framework_demo.git"
        print os.popen(cmd).read()

    def job_Mac(self):
        cmd = "pybot --variable BROWSER:safari --outputdir safari_dir --include demo --xunit output_xunit.xml --xunitskipnoncritical ./YX_RFUI_Framework_demo/Test/YX_Subscriptions/test_suite_examples.txt"
        print os.popen(cmd).read()

    def job_Windows(self):
        print "\n\n>>>here is from Windows\n\n"

        cmd = "C:\Python27\python -m robot.run " \
              "--include=demo " \
              "--xunit=xunitOutput.xml " \
              "--outputdir=D:\JENKINS_hzqa_CI\workspace\yixin-WebUiTest-xdq\RFUI_outputs_dir " \
              "D:\JENKINS_hzqa_CI\workspace\yixin-WebUiTest-xdq\YX_RFUI_Framework_demo\Test\YX_Subscriptions"
        print os.popen(cmd).read()

    def job_Linux(self):
        print "[info]:Linux fx() need added in future ;-)"


if __name__ == '__main__':

    MyParser = MyParser()
    MyParser.create_output_dir()
    MyParser.get_newest_apk()
    MyParser.get_device_info()
    MyParser.get_gitbucket()

    uname_str = platform.system()
    print uname_str
    mac_arch = re.search("Darwin",uname_str)
    win_arch = re.search("Windows",uname_str)
    linux_arch = re.search("Linux",uname_str)

    t2= 'None'
    if mac_arch:
        MyParser.job_Mac()
    elif win_arch:
        MyParser.job_Windows()
    elif linux_arch:
        MyParser.job_Linux()
    else:
        print "[err]:can NOT detect OS type :-("
