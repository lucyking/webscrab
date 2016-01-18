# coding=utf-8
"""A automatic CI script support multiple OS.
"""
import os
import re
import sys
import urllib
import urllib2
import shutil
import getopt
import platform
from time import ctime
from HTMLParser import HTMLParser


class MyParser(HTMLParser):
    """the main class
    """
    xunit = 'NULL'
    version = 'NULL'
    include = 'NULL'
    testcase = 'NULL'
    outputdir = 'NULL'
    input_cmd = ''

    dev_model = 'NULL'
    dev_os_version = 'NULL'
    dev_manufacturer = 'NULL'

    resault = 'NULL'
    pwd = "/your/script/workspace/path"

    def __init__(self):
        HTMLParser.__init__(self)

    @staticmethod
    def get_opt_content(opt):
        """parse input argv to archive --outputdir,etc.
        :return: string
        """
        opts, args = getopt.getopt(sys.argv[1:], "hvi:o:x:",
                                   ["help", "version", "outputdir=",
                                    "include=", "xunit=", "testcase="])
        for op, value in opts:
            if op == opt:
                return value

    def parse_argv(self):
        opts, args = getopt.getopt(sys.argv[1:], "hvi:o:x:",
                                   ["help", "version", "outputdir=",
                                    "include=", "xunit=", "testcase="])
        for op, value in opts:
            if op == "-h" or op == "--help":
                self.print_usage()
                sys.exit()

    @staticmethod
    def  print_usage():
        """print help manual
        :return: help manual  screen  output
        """
        print "\n[Option]\n=========="
        print "%-16s%-10s" % ("-h --help", " \tprint this help manual")
        print "%-16s%-10s" % ("-d --outputdir dir", "\tOutput files path.")
        print "%-16s%-10s" % ("-i --include tag ", "\tInclude test cases.")
        print "%-16s%-10s" % ("-e --exclude tag ", "\tExclude test cases.")
        print "%-16s%-10s" % ("-x --xunit file ", "\tCreate xUnit file.")
        print "\n[Examples]\n=========="
        print "[Mac]:\v" \
              "python " \
              "ci_example.py " \
              "--include=Test" \
              "--outputdir=output " \
              "--xunit=xunitOutput.xml " \
              "./YX_RFUI_Framework_demo/Test/YX_Subscriptions/Mobile_Android"
        print "[Win]:\v" \
              r"C:\Python27\python " \
              r" D:\*\ci_example.py " \
              r"--include=aostest " \
              r"--outputdir=D:\*\output  " \
              r"--xunit=xunitOutput.xml " \
              r"D:\*\Mobile_Android "
        sys.exit()

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name, value in attrs:
                if name == 'href':
                    self.resault = value  # merged by the latest version info

    def getHtml(self, url):
        page = urllib.urlopen(url)
        html = page.read()
        return html

    def start_appium(self):
        # cmd = 'start /b appium'
        # cmd = 'nohup appium & '
        # cmd = 'echo `nohup /usr/local/bin/appium &` &'
        cmd = 'ps aux'
        print "-------%s-------" % ctime()
        print os.popen(cmd).read()

    def manage_output_dir(self):
        output_dir = self.get_opt_content("--outputdir")
        if os.path.exists(output_dir):
            try:
                shutil.rmtree(output_dir)
                os.mkdir(output_dir)
            except IOError, error:
                print IOError, ">>>", error
        else:
            try:
                os.mkdir(output_dir)
            except IOError, error:
                print IOError, ">>>", error

    def get_newest_apk(self):
        html = self.getHtml('http://10.240.129.99/nightly/')
        self.feed(html)  # -->def handle_starttag():
        print "-------%s-------" % ctime()
        apk_version = self.resault
        apk_version = apk_version.replace('/', '')

        flip = open('test_dev_info.properties', 'w')
        flip.write('android_app_version=' + apk_version + '\n')
        flip.close()

        # remove old apk
        for item in os.listdir('./'):
            if os.path.splitext(item)[1] == ".apk":
                if item != (apk_version + ".apk"):
                    os.remove(item)

        if os.path.exists('./' + apk_version + '.apk'):
            print "the Apk already up-to-date\n"
        else:
            # download newest apk
            download_url = "http://10.240.129.99/nightly/" \
                           + apk_version + '/' + apk_version + ".apk"
            flip = urllib2.urlopen(download_url)
            self.pwd = sys.path[0]
            print self.pwd
            data = flip.read()
            filename = apk_version + ".apk"
            with open(filename, "wb") as code:
                code.write(data)
            print "Download Done!"

        # link newest apk to ./Res*/yixin_test.apk
        # Win:ln <src>  <des>  |  Mac/Linux: ln -s <src> <des>
        uname_str = platform.system()
        os_arch = re.search("Windows", uname_str)
        if os_arch:
            cmd = "copy /y  .\\" + apk_version + ".apk" \
                  + "   " + ".\\Resources\\yixin_test.apk"
            print os.popen(cmd).read()
        else:
            cmd = "cp -f ./" + apk_version + ".apk" \
                  + "   " + " ./YX_RFUI_Framework/Resources/yixin_test.apk"
            print os.popen(cmd).read()

    @staticmethod
    def parse_info(source, target):
        resault = re.search(r"("+target+r")(\S+)", source).group(2)
        return resault

    def get_device_info(self):
        """:return Motorola XT1080 4.4.4 ,etc.
        """
        cmd = "adb devices"
        dev_info = os.popen(cmd).read()
        if len(dev_info) > len('List of devices attached\n\n'):
            cmd = "adb shell cat /system/build.prop"
            dev_info = os.popen(cmd).read()
            tag = re.search(r"ro.product", dev_info)
            if tag:
                self.dev_manufacturer = \
                    re.search(r"(ro.product.manufacturer=)(\S+)", dev_info).group(2)
                self.dev_model = \
                    re.search(r"(ro.product.model=)(\S+)", dev_info).group(2)
                self.dev_os_version = \
                    re.search(r"(ro.build.version.release=)(\S+)", dev_info).group(2)
                """
                s1= "ro.product.manufacturer="
                s2 = "ro.product.model="
                s3 = "ro.build.version.release="
                self.dev_manufacturer = self.parse_info(dev_info,s1)
                self.dev_model = self.parse_info(dev_info,s2)
                self.dev_os_version = self.parse_info(dev_info,s3)
                """
                print '>>>' + self.resault.replace('/', '')
                print '>>>' + self.dev_manufacturer,
                print self.dev_model,
                print self.dev_os_version
                flip = open('test_dev_info.properties', 'a')
                flip.write('android_dev_name=' + self.dev_manufacturer + '\n')
                flip.write('android_dev_model=' + self.dev_model + '\n')
                flip.write('android_version=' + self.dev_os_version + '\n')
                flip.close()
            else:
                print "\n\n>>>[x]:No device connect!\n\n"
                sys.exit()
        else:
            print "\n\n>>>[x]:No device connect!\n\n"
            sys.exit()

    def get_gitbucket(self):
        """pull remote repo to current dir
        """
        cmd = "git clone https://git.hz.netease.com/git/yxplusQA/YX_RFUI_Framework_demo.git"
        print os.popen(cmd).read()

    def job_Mac(self):
        """Mac's job
        """
        print "\n\n>>>here is from Mac\n\n"
        cmd = ' '.join(self.input_cmd)
        cmd = 'pybot' + ' ' + cmd
        print os.popen(cmd).read()

    def job_Windows(self):
        """Win's job
        """
        print "\n\n>>>here is from Windows\n\n"
        cmd = ' '.join(self.input_cmd)
        cmd = r'C:\Python27\python -m robot.run' + ' ' + cmd
        print os.popen(cmd).read()

    def job_Linux(self):
        """Linux's job
        """
        print "[info]:Linux fx() need added in future ;-)"

    def job_operate(self):
        """run corresponding job according to current OS system
        """
        uname_str = platform.system()
        if re.search("Darwin", uname_str):
            self.get_gitbucket()  # git clone *_demo
            self.job_Mac()
        elif re.search("Windows", uname_str):
            self.job_Windows()
        elif re.search("Linux", uname_str):
            self.get_gitbucket()  # git clone *_demo
            self.job_Linux()
        else:
            print "[x]:can NOT detect OS type :-("


if __name__ == '__main__':

    parse = MyParser()
    parse.input_cmd = sys.argv[1:]
    if len(sys.argv) == 1:
        parse.get_device_info()  # adb shell cat /system/build.prop
        parse.print_usage()
    parse.parse_argv()

    parse.manage_output_dir()  # mkdir ./RFUI_outputs_dir
    parse.get_newest_apk()  # wget latest.apk
    parse.get_device_info()  # adb shell cat /system/build.prop
    # parse.get_gitbucket()  # will uncommented  latter
    parse.job_operate()
