class CacheEvictor:
    def __init__(self, strategy, max_size) -> None:
        self.strategy = strategy
        self.max_size = max_size

    def evict(self, cache):
        return self.strategy.evict()
