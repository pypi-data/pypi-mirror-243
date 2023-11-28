FROM python:3.11

RUN python3 -m pip uninstall -y pychassislib
# 拷贝依赖
COPY . /app
# 设置工作路径
WORKDIR /app
# 安装依赖
RUN python3 -m pip install -i https://mirrors.cloud.tencent.com/pypi/simple --trusted-host=mirrors.cloud.tencent.com pdm>=2.10.1
RUN python3 -m pdm install
# 启动时运行命令
CMD ["sh", "docker-deploy.sh", "./body_record/config.yml", "body_record.body_record"]