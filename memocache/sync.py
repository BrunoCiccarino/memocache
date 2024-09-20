import threading

class CacheLock:
    def __init__(self) -> None:
        self.lock = threading.Lock()

    def acquire(self) -> None:
        self.lock.acquire()

    def release(self) -> None:
        self.lock.release()

cache_lock = CacheLock()
