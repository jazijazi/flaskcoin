import os

class Config:
    # pass
    # SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    # SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS' , False)
    # SECRET_KEY=os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://root:root123@localhost:5432/coindb'
    #Admin Theme
    # FLASK_ADMIN_SWATCH = 'Superhero'

    #CELERY
    from kombu import Exchange, Queue
    default_exchange = Exchange('default', type='direct')
    task_queues = (
        Queue('high_tasks',exchange=default_exchange, routing_key='high.#',queue_arguments={'x-max-priority': 10}),
        Queue('medium_tasks',exchange=default_exchange, routing_key='medium.#',queue_arguments={'x-max-priority': 5}),
        Queue('low_tasks',exchange=default_exchange, routing_key='low.#',queue_arguments={'x-max-priority': 1}),
    )
    task_default_queue = 'medium_tasks'
    task_default_exchange = 'default'
    task_default_exchange_type = 'topic'
    #its for redis to use priority like amqp
    broker_transport_options = {'queue_order_strategy': 'priority',}


class Development(Config):
    DEBUG = True
    broker_url = 'redis://localhost:6379'
    result_backend = 'redis://localhost:6379'
    enable_utc = True 
    timezone = 'Asia/Tehran'
    
class Production(Config):
    DEBUG = False