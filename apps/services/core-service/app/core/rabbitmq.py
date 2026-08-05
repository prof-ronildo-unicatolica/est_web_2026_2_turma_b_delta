import json
import aio_pika
from app.core.config import settings

async def publish_event(queue_name: str, event_data: dict):
    """
    Publica um evento JSON assincronamente em uma fila específica do RabbitMQ.
    """
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        
        # Declara a fila (cria caso nao exista)
        queue = await channel.declare_queue(queue_name, durable=True)
        
        # Converte o payload para JSON
        message_body = json.dumps(event_data).encode("utf-8")
        
        # Envia a mensagem para a fila
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=message_body,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            ),
            routing_key=queue.name
        )
