# 计蒜客实训项目环境配置完全指南

## 0 综述

此项目环境主要由以下项目组成：
- 适用于 Linux 的 Windows 子系统 (Ubuntu 18.04)
- Python 3.7.0 (pip 18.0 / setuptools 40.0.0)
- Apache2 2.4.29
- MySQL 5.7.23
- Node.js 10.8.0 (npm 6.2.0)
- vue-cli 3.0.0
- Django 2.1

以下的代码最好复制一行执行一行，不要批量复制。

## 1 安装 WSL

1. 确保在“控制面板 >> 程序和功能 >> 启用或关闭 Windows 功能”里已经开启了“适用于 Linux 的 Windows 子系统”。

2. 在 Microsoft Store 里安装 Ubuntu 。

3. 安装完成后打开 Ubuntu ，进行初始化配置，此时需要设置一个用户名和密码。

4. 初始化完成后，关闭 Ubuntu ，以管理员模式打开命令提示符，执行

    ```
    ubuntu config --default-user root
    ```

    以默认以 root 用户登录系统。

## 2 配置 WSL 系统环境

1. 再次打开 Ubuntu ，现在应该已经是以 root 身份登陆系统了。

2. 下面将系统软件源切换为清华大学软件源。
    + 删除原有软件源：

        ```
        rm /etc/apt/sources.list
        ```

    + 添加新软件源：

        ```
        nano /etc/apt/sources.list
        ```

    + 在打开的文本编辑器里键入该链接中的内容：

        ```
        deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic main restricted universe multiverse
        deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-updates main restricted universe multiverse
        deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-backports main restricted universe multiverse
        deb http://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-security main restricted universe multiverse
        ```

        编辑完成后，使用 Ctrl+O 保存，回车确定，再使用 Ctrl+X 退出。

3. 接下来更新系统。注意此步需要较长时间。如果中间出现选择项就选第一项。可以忽略里面的警告。

    ```
    apt update
    apt dist-upgrade
    apt autoremove
    ```

## 3 安装 Apache2 和 MySQL

1. 安装 Apache2 。

    ```
    apt install apache2
    ```

2. 安装 MySQL 。注意 Windows 中如果已经安装了 MySQL 需要先停止 MySQL 服务。

    ```
    apt install mysql-server mysql-client
    ```

## 4 安装 Node.js 以及 vue-cli

1. 添加 Node.js 10.x 安装源。

    ```
    curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
    ```

2. 安装 Node.js 和 npm 。

    ```
    apt install nodejs
    ```

3. 安装 @vue/cli 。

    ```
    npm install -g @vue/cli --registry=https://registry.npm.taobao.org
    ```

4. 安装 @vue/cli-init 。

    ```
    npm install -g @vue/cli-init --registry=https://registry.npm.taobao.org
    ```

5. 安装 webpack-dev-server 。

    ```
    npm install -g webpack-dev-server --registry=https://registry.npm.taobao.org
    ```

## 5 安装 Python 3.7

1. 安装 git / g++ / make 。

    ```
    apt install git g++ make
    ```

2. 安装一些必要的依赖包。

    ```
    apt install libffi-dev libbz2-dev libssl-dev libreadline6 libreadline6-dev
    apt install libsqlite3-dev zlib1g-dev libncurses5 libncurses5-dev libncursesw5
    apt install libgdbm-dev liblzma-dev uuid-dev
    ```

3. 安装 pyenv 。

    ```
    git clone git://github.com/yyuu/pyenv.git ~/.pyenv
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc
    exec $SHELL -l
    ```

4. 下载并编译 Python 3.7.0 。

    ```
    pyenv install 3.7.0 -v
    ```

5. 安装完成之后，需要使用如下命令对数据库进行更新。

    ```
    pyenv rehash
    ```

6. 设置全局 Python 版本。

    ```
    pyenv global 3.7.0
    ```

7. 配置 venv 。

    ```
    python -m venv ~/venv
    source ~/venv/bin/activate
    ```

8. 更新 pip (venv 中)。

    ```
    python -m pip install --upgrade pip
    ```

9. 更新 setuptools (venv 中)。

    ```
    python -m pip install --upgrade setuptools
    ```

## 6 安装 Django 和 mysqlclient

1. 安装必要依赖库。

    ```
    apt install libmysqlclient-dev
    ```

2. 安装 Django (venv 中)。

    ```
    pip install django
    ```

3. 安装 mysqlclient  (venv 中)。

    ```
    pip install mysqlclient
    ```

## 7 链接工程文件夹

1. 从项目仓库克隆项目文件夹到你想要的位置。这里以 D:/example 为例。

    ```
    git clone https://se.jisuanke.com/2100-lab/Group1.git
    ```
2. 链接项目文件夹到 WSL 的 /root/project 目录，路径根据你上面设定的路径变化。

    ```
    ln -s /mnt/d/example ~/project
    ```

3. 这样，D:/example 中的文件就被映射到了 ~/project 中。
