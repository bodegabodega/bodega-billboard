import time

class TimeKeeper(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print('Creating the object')
            cls._instance = super(TimeKeeper, cls).__new__(cls)
            cls._instance.listeners = {}
        return cls._instance
    
    def add_listener(self, name, fn, interval=3600):
        dict = {'fn': fn, 'interval': interval, 'last_run': time.time()}
        self.listeners[name] = dict
    
    def remove_listener(self, name):
        if name in self.listeners:
            del self.listeners[name]
    
    def update(self):
        for listener in self.listeners.values():
            if time.time() - listener['last_run'] > listener['interval']:
                listener['last_run'] = time.time()
                listener['fn']() 