import json
from channels.generic.websocket import AsyncWebsocketConsumer
import aioredis
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
import asyncio
from .models import *


import json
from channels.generic.websocket import AsyncWebsocketConsumer
import aioredis

import redis

# Создание экземпляра клиента Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

class EchoConsumer(AsyncWebsocketConsumer):


    async def connect(self):
        self.user = await database_sync_to_async(self.get_user)(self.scope["session"])
        self.room_group_name = f'user_{self.user.id}'
        self.followings = await database_sync_to_async(self.user.getFollowings)()
        print(self.followings)


        for i in self.followings:
            await self.channel_layer.group_add(
                f"follow_{i.destination.id}",
                self.channel_name
            )
        await self.channel_layer.group_add(
                f"follow_{self.user.id}",
                self.channel_name
            )

        # Присоединение к группе
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.channel_layer.group_add(
            'broadcast_group',
            self.channel_name
        )

        await self.accept()


        await self.send(text_data=json.dumps({
            'message': f"Hello {self.user.nickname}"
        }))

    def get_user(self, session):
        print("trying to get user")
        u = User.AuthBySession(session)
        print(u.getPublicData())
        return u



    async def disconnect(self, close_code):
        # Отсоединение от группы
        for i in self.followings:
            await self.channel_layer.group_discard(
                f"follow_{i.destination.id}",
                self.channel_name
            )
        await self.channel_layer.group_discard(
                f"follow_{self.user.id}",
                self.channel_name
            )

        # Присоединение к группе
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        await self.channel_layer.group_discard(
            'broadcast_group',
            self.channel_name
        )

    # Получение сообщения от WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Отправка обратного сообщения в WebSocket
        await self.send(text_data=json.dumps({
            'message': message[::-1]  # Сообщение наоборот
        }))


    async def send_message_to_group(self, message):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Получение сообщения от группы
    async def chat_message(self, event):
        message = event['message']

        # Отправка сообщения
        await self.send(text_data=json.dumps({
            'message': message
        }))


    async def send_broadcast_message(self, message):
        await self.channel_layer.group_send(
            'broadcast_group',
            {
                'type': 'broadcast_message',
                'message': message
            }
        )

    # Получение сообщения от общей группы
    async def broadcast_message(self, event):
        message = event['message']

        # Отправка сообщения всем пользователям в группе
        await self.send(text_data=json.dumps({
            'message': message
        }))





# # Настройка клиента Redis
# r = redis.Redis(host='localhost', port=6379, db=0)

# class EchoConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         # Сохраняем текущее подключение в Redis
#         r.set(self.channel_name, 1)
#         # Отправляем приветственное сообщение
#         await self.send(text_data=json.dumps({'message': 'Добро пожаловать!'}))

#     async def disconnect(self, close_code):
#         # Удаляем подключение из Redis
#         r.delete(self.channel_name)

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         # Отправляем перевернутое сообщение
#         await self.send(text_data=json.dumps({'message': message[::-1]}))

#     @classmethod
#     async def send_to_everyone(cls, message):
#         channel_layer = get_channel_layer()
#         # Получаем все текущие подключения из Redis
#         current_connections = r.keys('*')
#         for connection in current_connections:
#             await channel_layer.send(connection.decode('utf-8'), {
#                 'type': 'websocket.send',
#                 'text': message
#             })



# class EchoConsumer(AsyncWebsocketConsumer):
#     redis = None

#     @classmethod
#     async def connect_to_redis(cls):
#         if not cls.redis:
#             cls.redis = await aioredis.from_url("redis://localhost", encoding='utf-8', decode_responses=True)

#     async def connect(self):
#         await self.connect_to_redis()
#         await self.accept()
#         # Добавление текущего подключения в Redis
#         await self.redis.sadd("connected_users", self.channel_name)

#     async def disconnect(self, close_code):
#         # Удаление текущего подключения из Redis
#         await self.redis.srem("connected_users", self.channel_name)

#     async def receive(self, text_data):
#         # Получение и переворачивание сообщения
#         message = json.loads(text_data)["message"]
#         reversed_message = message[::-1]
#         # Отправка перевернутого сообщения обратно
#         await self.send(text_data=json.dumps({
#             "message": reversed_message
#         }))

#     @classmethod
#     def send_to_everyone_sync(cls, message):
#         # Обертка для синхронного вызова асинхронного метода
#         database_sync_to_async(cls.send_to_everyone)(message)

#     @classmethod
#     async def send_to_everyone(cls, message):
#         await cls.connect_to_redis()
#         # Получение всех подключений из Redis
#         connections = await cls.redis.smembers("connected_users")
#         # Отправка сообщения каждому подключенному пользователю
#         for user in connections:
#             channel_layer = get_channel_layer()
#             await channel_layer.send(
#                 user,
#                 {
#                     'type': 'echo.message',
#                     'text': json.dumps({"message": message})
#                 }
#             )
#     # Обработчик для вашего собственного типа сообщения
#     async def echo_message(self, event):
#         await self.send(event['text'])
# cd ..
# ..\env\Scripts\activate
# cd project
# python manage.py runserver
# daphne -p 8666 webProject.asgi:application

# python manage.py shell
# quit()