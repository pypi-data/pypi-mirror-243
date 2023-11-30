# Retrieving and processing user data from Redis

import json
import redis

from .basedefs import *

# This is the somewhat inaptly named Redis attribute for data about an account's
# access permissions to data with higher protection needs -- currently SAP/KIS,
# SAP-HR, and Zone7 file shares.
redis_sda_attribute = "sensible_data_access"


def getsecret_json(key_path):
    """Get a secret from a json file. key_path is keys separated with slashes."""
    with open(config.secrets_json_file) as f:
        data = json.loads(f.read())
    for key in key_path.split("/"):
        data = data.get(key)
        if data is None:
            raise KeyError(
                f"key path '{key_path}' not found in '{config.secrets_json_file}'")
    return data

redis_connection = None

def get_redis_connection():
    """Get a connection to the configured Redis server (config.redis)."""
    global redis_connection
    if redis_connection is None:
        redis_connection = redis.Redis(
            unix_socket_path=config.redis_limes.unix_socket_path,
            password=getsecret_json(config.redis_limes.secrets_json_key)
        )
    return redis_connection


def get_redis(uid, redismap):
    data = get_redis_connection().get(f"{redismap}::{uid}")
    if data:
        return json.loads(data)
    return None


def has_sapkis_access(uid):
    """Return True iff `uid` has access to SAP/KIS."""
    accesses = get_redis(uid, redis_sda_attribute)
    return bool(accesses and "SAP" in accesses)


def has_saphr_access(uid):
    """Return True iff `uid` has access to SAP-HR."""
    accesses = get_redis(uid, redis_sda_attribute)
    return bool(accesses and "SAP-HR" in accesses)
