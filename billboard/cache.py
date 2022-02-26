import time

class Cache(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Cache, cls).__new__(cls)
            cls._instance.cache = {}
        return cls._instance

    def get(self, key):
        if key in self.cache and self.cache[key]["til"] > time.time():
            return self.cache[key]["value"]
        else:
            return None

    def set(self, key, value, ttl=3600):
        self.cache[key] = {
            "value": value,
            "til": time.time() + ttl
        }

