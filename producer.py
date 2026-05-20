import asyncio
import sys

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import rabbitpy
from configuracoes import url_amqp, EXCHANGE, FILAS, RK_COMIDA, RK_BEBIDA, RK_CAIXA

NOME_MESA = 'Mesa 1'

PEDIDOS = [
    (RK_COMIDA, f'{NOME_MESA}: X-Burguer'),
    (RK_BEBIDA, f'{NOME_MESA}: Suco de Laranja'),
    (RK_CAIXA,  f'{NOME_MESA}: R$ 35,00'),
]


def preparar_infraestrutura(canal):
    exchange = rabbitpy.Exchange(canal, EXCHANGE)
    exchange.declare()
    for nome_fila, routing_key in FILAS:
        fila = rabbitpy.Queue(canal, nome_fila, durable=True, auto_delete=False)
        fila.declare()
        fila.bind(exchange, routing_key)
    return exchange


def publicar_pedidos(canal, exchange):
    print(f'[Garçom] Registrando pedidos da {NOME_MESA}...')
    for routing_key, conteudo in PEDIDOS:
        msg = rabbitpy.Message(canal, conteudo)
        msg.publish(exchange, routing_key)
        print(f'  → {conteudo}')


def main():
    with rabbitpy.Connection(url_amqp()) as conn:
        with conn.channel() as canal:
            exchange = preparar_infraestrutura(canal)
            publicar_pedidos(canal, exchange)


if __name__ == '__main__':
    main()
