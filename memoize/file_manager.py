import os
import pickle

CACHE_DIR = os.path.join(os.getcwd(), '.memocache')

def ensure_cache_dir():

    if not os.path.exists(CACHE_DIR):
        print(f"Criando diretório de cache: {CACHE_DIR}")
        os.makedirs(CACHE_DIR)

def save_to_file(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)  
    with open(path, 'wb') as f:
        f.write(data)

def load_from_file(key):
    
    ensure_cache_dir()  
    cache_file = os.path.join(CACHE_DIR, f"{key}.memo")
    if os.path.exists(cache_file):
        with open(cache_file, 'rb') as f:
            return pickle.load(f)
    return None
