# coding=utf-8
import urllib, urllib2
import sys, os,re, threading
from time import ctime, sleep
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
                    self.resault = value  # merge with the latest apk

    def getHtml(self, url):
        page = urllib.urlopen(url)
        html = page.read()
        return html

    def startAppium(self):
        # cmd = 'start /b appium'
        # cmd = 'nohup appium & '
        # cmd = 'echo `nohup /usr/local/bin/appium &` &'
        cmd = 'date'
        print "-------%s-------" % ctime()
        print os.popen(cmd).read()

    def job_Mac(self):
        # cmd = "rm ./*"
        # print os.popen(cmd).read()

        cmd = " git clone https://git.hz.netease.com/git/hzxiadaqiang/Script.git"
        print os.popen(cmd).read()

        cmd ="cp -r ./Script/*   ./  && rm -r ./Script "
        print os.popen(cmd).read()

        cmd = "mkdir RFUI_outputs_dir"
        print os.popen(cmd).read()
        # cmd = "touch ./RFUI_outputs_dir/log.html ./RFUI_outputs_dir/"

        cmd = "git clone https://git.hz.netease.com/git/yxplusQA/YX_RFUI_Framework_demo.git"
        print os.popen(cmd).read()

        # cmd = "wget https://git.hz.netease.com/hzxiadaqiang/Script/blob/master/webscrab.py?raw=true && mv webscrab.py?raw=true webscrab.py"
        # print os.popen(cmd).read()

        html = self.getHtml('http://10.240.129.99/nightly/')
        apk_list = self.feed(html)
        print "-------%s-------" % ctime()
        print apk_list
        print self.resault
        apk_version = self.resault
        apk_version = apk_version.replace('/', '')
        print apk_version

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
            with open(filename, "wb") as code:
                code.write(data)
            print "Download Done!"

        # rm the old apk
        cmd = "rm ./YX_RFUI_Framework_demo/Resources/yixin_test.apk"
        print os.popen(cmd).read()
        # script alongside the Res dir
        cmd = "ln -s ./" + apk_version + ".apk" + "   ./YX_RFUI_Framework_demo/Resources/yixin_test.apk"
        print os.popen(cmd).read()

        cmd = "pybot --variable BROWSER:safari --outputdir safari_dir --include demo --xunit output_xunit.xml --xunitskipnoncritical ./YX_RFUI_Framework_demo/Test/YX_Subscriptions/test_suite_examples.txt"
        # cmd = "ps aux"
        # print "[%s]:" %ctime()
        print "-------%s-------" % ctime()
        print os.popen(cmd).read()

    def job_Windows(self):
        # cmd = "rm ./*"
        # print os.popen(cmd).read()

        cmd = " git clone https://git.hz.netease.com/git/hzxiadaqiang/Script.git"
        print os.popen(cmd).read()

        cmd ="cp -r ./Script/*   ./  && rm -r ./Script "
        print os.popen(cmd).read()

        cmd = "mkdir RFUI_outputs_dir"
        print os.popen(cmd).read()
        # cmd = "touch ./RFUI_outputs_dir/log.html ./RFUI_outputs_dir/"

        cmd = "git clone https://git.hz.netease.com/git/yxplusQA/YX_RFUI_Framework_demo.git"
        print os.popen(cmd).read()

        # cmd = "wget https://git.hz.netease.com/hzxiadaqiang/Script/blob/master/webscrab.py?raw=true && mv webscrab.py?raw=true webscrab.py"
        # print os.popen(cmd).read()

        html = self.getHtml('http://10.240.129.99/nightly/')
        apk_list = self.feed(html)
        print "-------%s-------" % ctime()
        print apk_list
        print self.resault
        apk_version = self.resault
        apk_version = apk_version.replace('/', '')
        print apk_version

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
            with open(filename, "wb") as code:
                code.write(data)
            print "Download Done!"
            sleep(8) # wait appium start

        # rm the old apk
        cmd = "rm ./YX_RFUI_Framework_demo/Resources/yixin_test.apk"
        print os.popen(cmd).read()
        # script alongside the Res dir
        cmd = "ln -s ./" + apk_version + ".apk" + "   ./YX_RFUI_Framework_demo/Resources/yixin_test.apk"
        print os.popen(cmd).read()

        cmd = "pybot --variable BROWSER:safari --outputdir safari_dir --include Androiddemo --xunit output_xunit.xml --xunitskipnoncritical ./YX_RFUI_Framework_demo/Test/YX_Subscriptions/test_suite_examples.txt"
        # cmd = "ps aux"
        # print "[%s]:" %ctime()
        print "-------%s-------" % ctime()
        print os.popen(cmd).read()


if __name__ == '__main__':

    MyParser = MyParser()

    cmd = 'uname -a'
    uname_str = os.popen(cmd).read()
    sys_arch = re.search("Kernel",uname_str)
    print sys_arch
    if sys_arch:
        t2 = threading.Thread(target=MyParser.job_Mac())
    else:
        t2 = threading.Thread(target=MyParser.job_Windows())
    threads = []
    t1 = threading.Thread(target=MyParser.startAppium())
    threads.append(t1)
    threads.append(t2)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
