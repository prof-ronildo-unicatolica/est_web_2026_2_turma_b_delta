import asyncio
import json
from datetime import datetime
import aio_pika
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        try:
            # Carrega os dados da mensagem
            data = json.loads(message.body.decode("utf-8"))
            print(f"[Worker] Mensagem recebida: {data}")

            # Conecta ao MongoDB
            mongo_client = AsyncIOMotorClient(settings.MONGODB_URL)
            db = mongo_client[settings.MONGODB_DB]
            collection = db["logs_auditoria"]

            # Adiciona timestamp e salva no MongoDB
            log_document = {
                **data,
                "timestamp": datetime.utcnow().isoformat()
            }
            await collection.insert_one(log_document)
            print(f"[Worker] Log registrado com sucesso no MongoDB!")

        except Exception as e:
            print(f"[Worker] Erro ao processar mensagem: {str(e)}")

async def main():
    print(f"[Worker] Conectando ao RabbitMQ: {settings.RABBITMQ_URL}")
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
    
    async with connection:
        channel = await connection.channel()
        
        # Define prefetch count para balancear carga
        await channel.set_qos(prefetch_count=10)
        
        # Declara a fila de auditoria
        queue = await channel.declare_queue("audit.logs", durable=True)
        
        print("[Worker] Aguardando mensagens na fila 'audit.logs'...")
        await queue.consume(process_message)
        
        # Mantem o loop rodando indefinitivamente
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("[Worker] Parado pelo usuario.")
