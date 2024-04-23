from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from channels.testing import WebsocketCommunicator
from asgiref.sync import async_to_sync
import asyncio
import json
import logging

logger = logging.getLogger(__name__)

class ProctoringConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            await self.accept()
            logger.info("WebSocket connection established")
        except Exception as e:
            logger.error(f"Error during WebSocket connection: {e}")
            await self.close()

    async def disconnect(self, close_code):
        logger.info("WebSocket connection closed")
        await self.close()

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json['type']

            if message_type == 'start_proctoring':
                exam_id = text_data_json['exam_id']
                # Perform actions related to starting proctoring for the given exam_id
                # ...

                await self.send(text_data=json.dumps({
                    'message': 'Proctoring started successfully',
                }))
        except Exception as e:
            logger.error(f"Error during WebSocket message processing: {e}")

async def async_connect_proctoring_consumer(exam_id):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        channel_layer = get_channel_layer()
        channel_name = f"proctoring_exam_{exam_id}"

        communicator = WebsocketCommunicator(ProctoringConsumer.as_asgi(), f"/ws/proctoring/{channel_name}")

        connected, _ = await communicator.connect()
        return communicator if connected else None
    finally:
        loop.close()


