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

    def manage_file(self):
        cmd = "mkdir RFUI_outputs_dir"
        print os.popen(cmd).read()
        cmd = "cd .>./RFUI_outputs_dir/output.xml && cd . > ./RFUI_outputs_dir/log.html && cd . > ./RFUI_outputs_dir/log.png && cd . > ./RFUI_outputs_dir/xunitOutputs.xml"
        print os.popen(cmd).read()


    def get_device_info(self):
        """
        adb_info=`adb shell cat /system/build.prop`
        echo "adb_info: ${adb_info}"
        dev_manufacturer=`echo "${adb_info}" | grep ro.product.manufacturer | awk -F\= '{print $2}'`
        dev_model=`echo "${adb_info}" | grep ro.product.model | awk -F\= '{print $2}'`
        device_os_version=`echo "${adb_info}" | grep ro.build.version.release | awk -F\= '{print $2}'`
        echo "\ndev_manufacturer: ${dev_manufacturer}"
        echo "dev_model: ${dev_model}"
        echo "device_os_version: ${device_os_version}"
        """
        # cmd = "adb shell cat /system/build.prop "
        # cmd = "C:\Users\Administrator\AppData\Local\Android\sdk\platform-tools\adb.exe shell cat /system/build.prop"
        cmd = "adb.exe shell cat /system/build.prop"
        # p =subprocess.Popen(cmd,shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
        # dev_info = os.popen(cmd).read()
        # dev_info,stderr = p.communicate()
        dev_info,stderr=subprocess.Popen(cmd,shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
        print dev_info,stderr

        if dev_info:
            self.dev_manufacturer = re.search(r"(ro.product.manufacturer=)(\S+)",dev_info).group(2)
            self.dev_model = re.search(r"(ro.product.model=)(\S+)",dev_info).group(2)
            self.dev_os_version= re.search(r"(ro.build.version.release=)(\S+)",dev_info).group(2)
            print self.dev_manufacturer,self.dev_model,self.dev_os_version
            fl=open('test_dev_info.properties','w')
            fl.write('android_dev_name='+self.dev_manufacturer+'\n')
            fl.write('android_dev_model='+self.dev_model+'\n')
            fl.write('android_version='+self.dev_os_version+'\n')
            fl.close()
        else:
            print "dev_info-->Null"


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

    def job_Mac(self):
        # cmd = "rm ./*"
        # print os.popen(cmd).read()

        cmd = " git clone https://git.hz.netease.com/git/hzxiadaqiang/Script.git"
        print os.popen(cmd).read()

        cmd ="cp -r ./Script/*   ./  && rm -r ./Script "
        print os.popen(cmd).read()


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
        print "\n\n>>>here is from Windows\n\n"

        cmd = " git clone https://git.hz.netease.com/git/hzxiadaqiang/Script.git"
        print os.popen(cmd).read()

        cmd ="cp -r ./Script/*   ./  && rm -r ./Script "
        print os.popen(cmd).read()


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
        # "ln -s" don't work in Windows, use "ln" instead
        cmd = "ln  ./" + apk_version + ".apk" + "   ./YX_RFUI_Framework_demo/Resources/yixin_test.apk"
        print os.popen(cmd).read()

        cmd = "pybot --outputdir RFUI_outputs_dir --include Androiddemo --xunit output_xunit.xml --xunitskipnoncritical ./YX_RFUI_Framework_demo/Test/YX_Subscriptions/test_suite_examples.txt"
        # cmd = "pybot  --include Androiddemo  ./YX_RFUI_Framework_demo/Test/YX_Subscriptions/test_suite_examples.txt"
        # cmd = "ps aux"
        # print "[%s]:" %ctime()
        print "-------%s-------" % ctime()
        print os.popen(cmd).read()

    def job_Linux(self):
        print "[info]:Linux fx() need added in future ;-)"


if __name__ == '__main__':

    MyParser = MyParser()
    """
    cmd = 'uname -a'
    uname_str = os.popen(cmd).read()
    print "[arch]:",uname_str
    """
    MyParser.manage_file()

    uname_str = platform.system()
    print uname_str
    mac_arch = re.search("Darwin",uname_str)
    win_arch = re.search("Windows",uname_str)
    linux_arch = re.search("Linux",uname_str)

    t2= 'None'
    if mac_arch:
        t2 = threading.Thread(target=MyParser.job_Mac())
    elif win_arch:
        t2 = threading.Thread(target=MyParser.job_Windows())
    elif linux_arch:
        t2 = threading.Thread(target=MyParser.job_Linux())  # you can use job_Mac() temporary
    else:
        print "[err]:can NOT detect OS type :-("

    threads = []
    t1 = threading.Thread(target=MyParser.get_device_info())
    threads.append(t1)
    if t2 != 'None':
        threads.append(t2)
    for t in threads:
        t.start()
    for t in threads:
        t.join()