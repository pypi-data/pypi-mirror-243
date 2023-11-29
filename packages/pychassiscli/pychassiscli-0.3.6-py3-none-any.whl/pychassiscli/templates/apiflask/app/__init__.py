import os

# from dotenv import load_dotenv
from apiflask import APIFlask
from chassis.flask_nameko import FlaskPooledClusterRpcProxy

from app.config.config import Config
from app.util.common import basedir


rpc = FlaskPooledClusterRpcProxy()


def register_blueprints(apiflask_app):
    from app.api.v1 import create_v1

    apiflask_app.register_blueprint(create_v1(), url_prefix='/v1')


def load_app_config(app):
    """
    加载环境变量和配置类到app config
    """
    # 读取 .env
    # load_dotenv(os.path.join(basedir, '.apiflask.env'))
    # 读取配置类
    app.config.from_object('app.config.config.Config')


def load_rpc_client(apiflask_app):
    apiflask_app.config.update(dict(
        NAMEKO_AMQP_URI=str(Config.RABBITMQ_URI)
    ))
    rpc.init_app(apiflask_app, extra_config={
        'INITIAL_CONNECTIONS': 4,
        'MAX_CONNECTIONS': 30,
    })


def create_app():
    # http wsgi server 托管启动需指定读取环境配置
    # load_dotenv(os.path.join(basedir, '.apiflaskenv'))
    app = APIFlask(__name__, title='Body Record API', version='1.0.0', docs_ui='redoc')
    app.servers = [
        {
            'name': 'Production Server',
            'url': 'https://www.bearcatlog.com/pzx/'
        }
    ]
    load_app_config(app)
    register_blueprints(app)
    load_rpc_client(app)
    return app