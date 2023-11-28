FROM python:3.11

RUN python3 -m pip uninstall -y pychassislib
# 拷贝依赖
COPY requirements.txt .
# 安装依赖
RUN python3 -m pip install -i https://mirrors.cloud.tencent.com/pypi/simple --trusted-host=mirrors.cloud.tencent.com pdm>=2.10.1
# RUN python3 -m pip install -i https://mirrors.cloud.tencent.com/pypi/simple --trusted-host=mirrors.cloud.tencent.com -r requirements.txt
RUN python3 -m pdm install