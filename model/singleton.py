import threading
from functools import wraps

def singleton(cls):
    """
    Decorator thread-safe para transformar uma classe em Singleton.
    """
    instances = {}
    lock = threading.Lock()  # lock compartilhado

    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:  # verificação rápida
            with lock:
                if cls not in instances:  # verificação dentro do lock
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance
