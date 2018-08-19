#!/bin/bash

# change sources list
rm /etc/apt/sources.list && touch /etc/apt/sources.list
echo 'deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic main restricted universe multiverse' >> /etc/apt/sources.list
echo 'deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-updates main restricted universe multiverse' >> /etc/apt/sources.list
echo 'deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-backports main restricted universe multiverse' >> /etc/apt/sources.list
echo 'deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-security main restricted universe multiverse' >> /etc/apt/sources.list

# upgrade system
apt update
apt dist-upgrade -y
apt autoremove -y

# install apache2 and mysql
apt install apache2 -y
apt install mariadb-server mariadb-client -y

# install nodejs and webpack-dev-server
curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
apt install nodejs -y
npm install -g webpack-dev-server --registry=https://registry.npm.taobao.org
npm config set registry https://registry.npm.taobao.org

# install necessary dependencies
apt install git g++ make -y
apt install libffi-dev libbz2-dev libssl-dev -y
apt install libreadline7 libreadline-dev libsqlite3-dev -y
apt install libncurses5 libncurses5-dev libncursesw5 -y
apt install libgdbm-dev liblzma-dev uuid-dev -y
apt install zlib1g-dev libmysqlclient-dev -y

# install pyenv
git clone https://se.jisuanke.com/AlumiK/pyenv_mirror.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

# install python 3.7.0
wget https://txy.ret.red/Python-3.7.0.tar.xz -P ~/.pyenv/cache
pyenv install 3.7.0 -v
pyenv rehash
pyenv global 3.7.0

# setup python virtual environment
python -m venv ~/venv
source ~/venv/bin/activate
rm -f ~/.pip/pip.conf
mkdir ~/.pip
touch ~/.pip/pip.conf
echo '[global]' >> ~/.pip/pip.conf
echo 'index-url = https://pypi.tuna.tsinghua.edu.cn/simple' >> ~/.pip/pip.conf
python -m pip install --upgrade pip
python -m pip install --upgrade setuptools

# link project files
ln -s /mnt/d/Group1 ~/project

# install project dependencies
cd ~/project/backend
pip install -r requirements.txt
cd ~/project/frontend
npm install

# setup git-hooks
cp ~/project/git-hooks/* ~/project/.git/hooks/
