# MyTypeOfShop Application Automation Scripts
> Scripts for automated orders and periodic database cleanup for the MyTypeOfShop application

### Installation
 Prerequisites:
  * NodeJS,
  * Selenium IDE runner
  * Chrome browser
  * MySQL Connector
1. NodeJS
   
```
    yum install -y gcc-c++ make
    curl -sL https://rpm.nodesource.com/setup_12.x | sudo -E bash -
    yum install nodejs
```
2. Selenium Side Runner
```
    npm install -g selenium-side-runner
```
3. Chrome
```  
    yum install wget
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
    yum install ./google-chrome-stable_current_*.rpm
    npm install -g chromedriver --unsafe-perm=true --allow-root
```
4. MySQL Connector
```
    yum install epel-release
    yum install python-pip
    pip install mysql-connector-python 
``` 
5. Under /root create a directory shopizer-automate and then clone the Project
```
    cd /root
    mkdir shopizer-automate
    cd shopizer-automate
    yum install git
    git clone https://github.com/XENTAURS/shopizer-automate.git
```
6. Copy shopizer_order_bot.service and shopizer_order_maint.service to /etc/systemd/system/
###
7. Run the following commands to enable the services
```buildoutcfg
    systemctl daemon-reload
    systemctl enable shopizer_order_bot.service
    systemctl enable shopizer_order_maint.service
```
8. Change permissions to allow execute on the scripts,  and then start them.
```buildoutcfg
    chmod +x order_bot.py
    chmod +x order_maint.py
    systemctl start shopizer_order_bot
    systemctl start shopizer_order_maint
```
Log file location:   /root/shopizer-automate/logs