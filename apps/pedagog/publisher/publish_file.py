import json, redis

from django.conf import settings


redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

def publish_file(chat_id, file_path, delay):
    message = json.dumps({
        'chat_id': chat_id,
        'file_path': file_path,
        'delay': delay
    })

    redis_client.publish('file_channel', message)