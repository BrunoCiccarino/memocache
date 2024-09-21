from memocache import memo
from standlib import Double

@memo
def main(a, b) -> Double:
    return a + b

print(main(8.5736877483, 5.36455264))