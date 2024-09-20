import collections
import time

class CacheBase:
    def __init__(self, max_size) -> None:
        self.max_size = max_size
        self.cache = {}

    def get(self, key):
        raise NotImplementedError

    def put(self, key, value):
        raise NotImplementedError

    def evict(self):
        raise NotImplementedError

class LRUCache(CacheBase):
    def __init__(self, max_size) -> None:
        super().__init__(max_size)
        self.order = collections.OrderedDict()

    def get(self, key):
        if key in self.cache:
            self.order.move_to_end(key)
            return self.cache[key]
        return None

    def put(self, key, value) -> None:
        if key in self.cache:
            self.order.move_to_end(key)
        self.cache[key] = value
        self.order[key] = time.time()
        if len(self.cache) > self.max_size:
            self.evict()

    def evict(self) -> None:
        oldest_key = next(iter(self.order))
        del self.cache[oldest_key]
        del self.order[oldest_key]

class LFUCache(CacheBase):
    def __init__(self, max_size) -> None:
        super().__init__(max_size)
        self.usage_counts = collections.Counter()  

    def get(self, key):
        if key in self.cache:
            self.usage_counts[key] += 1
            return self.cache[key]
        return None

    def put(self, key, value) -> None:
        if key in self.cache:
            self.usage_counts[key] += 1
        else:
            self.usage_counts[key] = 1
        self.cache[key] = value

        if len(self.cache) > self.max_size:
            self.evict()
    
    def evict(self) -> None:
        if not self.usage_counts:
            return  

    
        least_frequent_key = None
        least_frequent_count = float('inf')

        for key, count in self.usage_counts.items():
            if count < least_frequent_count:
                least_frequent_key = key
                least_frequent_count = count

    
        if least_frequent_key is not None:
            del self.cache[least_frequent_key]
            del self.usage_counts[least_frequent_key]

class FIFOCache(CacheBase):
    def __init__(self, max_size) -> None:
        super().__init__(max_size)
        self.queue = collections.deque()  

    def get(self, key):
        if key in self.cache:
            return self.cache[key]
        return None

    def put(self, key, value) -> None:
        if key not in self.cache:
            self.queue.append(key)
        self.cache[key] = value

        if len(self.cache) > self.max_size:
            self.evict()

    def evict(self) -> None:
        
        oldest_key = self.queue.popleft()
        del self.cache[oldest_key]