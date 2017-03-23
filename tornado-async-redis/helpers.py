""" Helper functions """
from toredis import Client
from tornado import gen
import config

GROUP_TYPE = {"total": "pvc", "mobile": "pvc_mobile", "pc": "pvc_mobile", "social": "pvc_social", "other": "pvc_other"}

async def get_count(content_id):
    """ Sends document id to redis and returns page view count as response. """
    response = await get_grouped_count("total", content_id)
    return response

async def get_grouped_count(group_type, content_id):
    """ Sends document id and group type to redis and returns page view count as response. """

    group_value = get_group_value(group_type)
    if group_value is None:
        return 0

    redis = Client()
    redis.connect(config.HOST,config.PORT)
    response = await gen.Task(redis.zcard, "{0}:{1}".format(group_value, content_id))
    return response

def get_group_value(group_type):
    """ Get type id for type string  """
    return GROUP_TYPE.get(group_type, None)