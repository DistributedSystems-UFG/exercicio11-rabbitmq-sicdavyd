import asyncio
import sys

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import rabbitpy
from configuracoes import url_amqp, EXCHANGE, FILAS, RK_COMIDA, RK_BEBIDA, RK_CAIXA

CARDAPIO_MESAS = [
    {
        'identificacao': 'Mesa 2',
        'itens': [
            (RK_COMIDA, 'Mesa 2: Frango Grelhado'),
            (RK_BEBIDA, 'Mesa 2: Refrigerante'),
            (RK_CAIXA,  'Mesa 2: R$ 28,00'),
        ],
    },
    {
        'identificacao': 'Mesa 3',
        'itens': [
            (RK_COMIDA, 'Mesa 3: Batata Frita'),
            (RK_COMIDA, 'Mesa 3: Salada Caesar'),
            (RK_BEBIDA, 'Mesa 3: Agua com Gas'),
            (RK_CAIXA,  'Mesa 3: R$ 42,00'),
        ],
    },
    {
        'identificacao': 'Mesa 4',
        'itens': [
            (RK_BEBIDA, 'Mesa 4: Vitamina de Banana'),
            (RK_CAIXA,  'Mesa 4: R$ 12,00'),
        ],
    },
]


def configurar_exchange(canal):
    exchange = rabbitpy.Exchange(canal, EXCHANGE)
    exchange.declare()
    for nome_fila, routing_key in FILAS:
        fila = rabbitpy.Queue(canal, nome_fila, durable=True, auto_delete=False)
        fila.declare()
        fila.bind(exchange, routing_key)
    return exchange


def enviar_mesa(canal, exchange, mesa: dict):
    print(f"\n[Garçom] Pedidos da {mesa['identificacao']}:")
    for routing_key, conteudo in mesa['itens']:
        msg = rabbitpy.Message(canal, conteudo)
        msg.publish(exchange, routing_key)
        print(f'  → {conteudo}')


def main():
    conn  = rabbitpy.Connection(url_amqp())
    canal = conn.channel()

    exchange = configurar_exchange(canal)

    for mesa in CARDAPIO_MESAS:
        enviar_mesa(canal, exchange, mesa)

    conn.close()
    print('\n[Garçom] Todos os pedidos foram enviados.')


if __name__ == '__main__':
    main()
