#!/bin/bash
rm /etc/apt/sources.list && touch /etc/apt/sources.list
echo 'deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic main restricted universe multiverse' >> /etc/apt/sources.list
echo 'deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-updates main restricted universe multiverse' >> /etc/apt/sources.list
echo 'deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-backports main restricted universe multiverse' >> /etc/apt/sources.list
echo 'deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-security main restricted universe multiverse' >> /etc/apt/sources.list
# 更新系统
apt-get update
apt-get dist-upgrade
apt-get autoremove
# 安装 Apache2 和 MySQL
apt-get install apache2
apt-get install mysql-server mysql-client
# 安装 Node.js 以及 vue-cli
curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
apt install nodejs
npm install -g @vue/cli --registry=https://registry.npm.taobao.org
npm install -g @vue/cli-init --registry=https://registry.npm.taobao.org
npm install -g webpack-dev-server --registry=https://registry.npm.taobao.org
# 安装一些必要的依赖包
apt install git g++ make
apt install libffi-dev libbz2-dev libssl-dev libreadline6 libreadline6-dev
apt install libsqlite3-dev zlib1g-dev libncurses5 libncurses5-dev libncursesw5
apt install libgdbm-dev liblzma-dev uuid-dev
# 安装 pyenv
git clone git://github.com/yyuu/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
exec $SHELL -l
# 下载并编译 Python 3.7.0
pyenv install 3.7.0 -v
pyenv rehash
pyenv global 3.7.0
# 更新 (venv 中)
python -m venv ~/venv
source ~/venv/bin/activate
python -m pip install --upgrade pip
python -m pip install --upgrade setuptools
# 安装 Django 和 mysqlclient
apt install libmysqlclient-dev
pip install django
pip install mysqlclient
# 链接文件夹
ln -s /mnt/d/Group1 ~/project