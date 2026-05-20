import asyncio
import sys

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import time
import rabbitpy
from configuracoes import url_amqp, FILA_COMIDA

TEMPO_PREPARO = 2  # segundos simulando preparo


def processar_pedido(msg) -> str:
    pedido = msg.body.decode()
    print(f'[Cozinha] Recebido: {pedido}')
    time.sleep(TEMPO_PREPARO)
    print(f'[Cozinha] Pronto:   {pedido}')
    msg.ack()
    return pedido


def iniciar_cozinha():
    print('[Cozinha] Aguardando pedidos de comida...')
    with rabbitpy.Connection(url_amqp()) as conn:
        with conn.channel() as canal:
            fila = rabbitpy.Queue(canal, FILA_COMIDA, durable=True, auto_delete=False)
            fila.declare()
            for msg in fila:
                processar_pedido(msg)


if __name__ == '__main__':
    iniciar_cozinha()
