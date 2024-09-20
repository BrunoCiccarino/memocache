import functools
import os
import hashlib
from .file_manager import save_to_file, load_from_file, CACHE_DIR
from .sync import cache_lock
from .serializer import serialize, deserialize
from .strategies import LRUCache, LFUCache, FIFOCache
from .evictor import CacheEvictor

""""A decorator that caches the results of function calls to avoid redundant computations,
improving performance in applications with intensive calculations. The cache is stored
in a `.memo` file within the `.memocache` directory. It supports various eviction
strategies (LFU, LRU, FIFO) to handle different data types. For complex data,
serializers are used to store them in the cache. Additionally, mechanisms for
cache synchronization are implemented.

**Args:**
    func (Optional[Callable]): The function to be decorated. If not provided,
                               returns a decorator that can be applied to a function.
    strategy (str, optional): The eviction strategy to use. Defaults to 'lfu'
                               (Least Frequently Used). Other options include 'lru'
                               (Least Recently Used) and 'fifo' (First-In-First-Out).
    max_size (int, optional): The maximum number of items to store in the cache.
                               Defaults to 100.
    ttl (int, optional): The time-to-live (TTL) in seconds for cached items.
                          If an item is not accessed within this time, it will
                          be evicted from the cache. Defaults to None (no TTL).

**Returns:**
    Callable: The decorated function.

**Raises:**
    ValueError: If an unsupported eviction strategy is provided.

**Example:**


from memoize.memo import memo

@memo(strategy='lru', max_size=500)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

result = fibonacci(35)  # This will be cached
result = fibonacci(35)  # This will be retrieved from the cache
    """

STRATEGY_MAP = {
    'lru': LRUCache,
    'lfu': LFUCache,  
    'fifo': FIFOCache
}

def memo(func=None, *, strategy='lfu', max_size=100, ttl=None):
    
    if func and callable(func):
        return _create_memo_decorator()(func)
    return _create_memo_decorator(strategy=strategy, max_size=max_size, ttl=ttl)

def _create_memo_decorator(strategy='lfu', max_size=100, ttl=None):
    def decorator(func):
        cache_class = STRATEGY_MAP.get(strategy.lower(), LFUCache)
        cache = cache_class(max_size)
        evictor = CacheEvictor(cache, max_size)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            serialized_key = serialize(key)

            hash_key = hashlib.md5(serialized_key).hexdigest()
            cache_path = os.path.join(CACHE_DIR, f"{hash_key}.memo")

            
            if os.path.exists(cache_path):
                try:
                    with open(cache_path, 'rb') as f:
                        cached_result = f.read()
                    return deserialize(cached_result)
                except Exception as e:
                    print(f"Erro ao carregar o arquivo de cache: {e}")

        
            result = func(*args, **kwargs)
            serialized_result = serialize(result)

            try:
                cache.put(hash_key, serialized_result)
                cache_lock.acquire()
                print(f"Salvando no arquivo: {cache_path}")
                save_to_file(cache_path, serialized_result)
            except Exception as e:
                print(f"Erro ao salvar o arquivo: {e}")
            finally:
                cache_lock.release()

            return result

        return wrapper

    return decorator
