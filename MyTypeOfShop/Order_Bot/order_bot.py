#!/usr/bin/python
# This script automates creation of an order against the MyTypeOfBlog app
# To change parameters such as the target IP address, modify the file Shopizer-Automate.side
# Prerequisites:
#  NodeJS, Selenium IDE runner, and Chrome browser
#   1. NodeJS
#    yum install -y gcc-c++ make
#    curl -sL https://rpm.nodesource.com/setup_12.x | sudo -E bash -
#    yum install nodejs
#   2. Selenium Side Runner
#    npm install -g selenium-side-runner
#   3. Chrome
#    wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
#    yum install ./google-chrome-stable_current_*.rpm
#    npm install -g chromedriver --unsafe-perm=true --allow-root
#
import subprocess
from subprocess import PIPE
import os
import datetime
import sys

class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("/root/shopizer-automate/logs/order_bot.log", "a",0)

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass

if __name__ == '__main__':
    if not os.path.exists('/root/shopizer-automate/logs'):
        os.mkdir('/root/shopizer-automate/logs')
    if os.path.exists('/root/shopizer-automate/logs/order_bot.log'):
        with open('/root/shopizer-automate/logs/order_bot.log') as f:
            orig_log = f.read()
        dt = datetime.datetime.now().strftime('%m-%d-%y_%H:%M:%S')
        with open ('/root/shopizer-automate/logs/order_bot_{0}.log'.format(dt),'w') as f:
            new_log = f.write(orig_log)
    else:
       os.mkdir('/root/shopizer-automate/logs')

    sys.stdout = Logger()

    side_files = ['MyTypeOfShop-KimberlyJones.side','MyTypeOfShop-JacobWest.side']

    cmds = []
    for file in side_files:
        cmds.append('selenium-side-runner -c "browserName=chrome chromeOptions.args=[headless,no-sandbox,disable-dev-shm-usage,disable-infobars]"'
                    ' /root/shopizer-automate/{0} --debug'.format(file))


    while True:
        for cmd in cmds:
            dt = datetime.datetime.now().strftime('%m-%d-%y %H:%M:%S')
            p = subprocess.Popen(cmd,stdout=PIPE,stderr=PIPE,shell=True)
            output = p.communicate()
            print('\n' + '--------------- {0} ---------------'.format(dt) + '\n')
            print(cmd)
            print(output[0])
            print(output[1])

