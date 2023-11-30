import json
import redis
import pickle
import hashlib

from generative_agent.tools import Vector_Database_Type

class Redis_Connector:
    def __init__(self, host: str = None, port: int = None, password: str = None):
        self.__host = host if host else "apn1-clear-vervet-33851.upstash.io"
        self.__port = port if port else 33851
        self.__password = password if password else "e248949a8af44f07aee8e6e23681862b"
        self.__client = redis.Redis(
            host=self.__host, port=self.__port, password=self.__password
        )

    def get_client(self):
        return self.__client

    def ping(self):
        return self.__client.ping()
