1.个人账号模拟登陆

2.店铺账号模拟登录（安全校验高，建议使用 3）

3.通过selenium+webdriver模拟登陆

4.api签名config->get_sign



注： 项目中的chromedriver 对应chrome 83版本

chromedriver与chrome版本镜像地址：
http://npm.taobao.org/mirrors/chromedriver/



linux 安装部署selenium:

1、安装chrome

  用下面的命令安装Google Chrome

  yum install https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm

  也可以先下载至本地，然后安装

  wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm

  yum install ./google-chrome-stable_current_x86_64.rpm

  安装必要的库

  yum install mesa-libOSMesa-devel gnu-free-sans-fonts wqy-zenhei-fonts

2、安装 chromedriver（末尾附chrome和chromedriver的对应版本）

  淘宝源（推荐）
  wget http://npm.taobao.org/mirrors/chromedriver/2.41/chromedriver_linux64.zip

  将下载的文件解压，放在如下位置
  unzip chromedriver_linux64.zip

  mv chromedriver /usr/bin/

  给予执行权限

  chmod +x /usr/bin/chromedriver

