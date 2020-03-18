import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Environmental variable configurations
    """

    """
    MySQL connection variable
    """
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)
    DATA_PERPAGE = 10

    """
    Security secret key
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')

    """
    Auth0 connection variable
    """
    DOMAIN = os.getenv('DOMAIN')

    """
    RabbitMQ connection variable
    """
    RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
    RABBITMQ_USERNAME: os.getenv('RABBITMQ_USERNAME')
    RABBITMQ_PASSWORD: os.getenv('RABBITMQ_PASSWORD')
    RABBITMQ_ROUTINGKEY = os.getenv('RABBITMQ_ROUTINGKEY')
    RABBITMQ_EXCHANGE = os.getenv('RABBITMQ_EXCHANGE')
    RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE')


    ELASTICSEARCH_INDEX = os.getenv('ELASTICSEARCH_INDEX')
    ELASTICSEARCH_HOST = os.getenv('ELASTICSEARCH_HOST')


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config_by_name = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig
)

key = Config.SECRET_KEY