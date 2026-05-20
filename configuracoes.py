import os

# Conexão RabbitMQ
MQ_HOST  = os.getenv('MQ_HOST',  'localhost')
MQ_USER  = os.getenv('MQ_USER',  'myuser')
MQ_SENHA = os.getenv('MQ_PASS',  'abc123')
MQ_VHOST = os.getenv('MQ_VHOST', 'my_vhost')

def url_amqp() -> str:
    return f'amqp://{MQ_USER}:{MQ_SENHA}@{MQ_HOST}:5672/{MQ_VHOST}'

# Exchange
EXCHANGE = 'lanchonete'

# Filas
FILA_COMIDA = 'pedidos_comida'
FILA_BEBIDA = 'pedidos_bebida'
FILA_CAIXA  = 'pedidos_caixa'

# Routing keys
RK_COMIDA = 'pedido.comida'
RK_BEBIDA = 'pedido.bebida'
RK_CAIXA  = 'pedido.caixa'

# Mapeamento fila → routing key
FILAS = [
    (FILA_COMIDA, RK_COMIDA),
    (FILA_BEBIDA, RK_BEBIDA),
    (FILA_CAIXA,  RK_CAIXA),
]
