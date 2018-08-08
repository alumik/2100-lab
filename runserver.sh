# 进入 Ubuntu
# 输入 chmod +x ~/project/runserver.sh
# 再输入 sh ~/project/runserver.sh 即可使 Django 服务器运行

#!/bin/bash
source ~/venv/bin/activate
cd ~/project/backend;
./manage.py runserver