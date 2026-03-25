import time

CACHE = {}

def set_cache(key,value):
    CACHE[key] = {
        "value":value,
        "time":time.time()
    }

def get_cache(key, ttl=300):
    data = CACHE.get(key)

    if not data:
        return None
    
    if time.time() - data["time"] > ttl:
        del CACHE[key]
        return None
    
    return data["value"]

def clear_cache_by_file(file_id: str):
    keys_to_delete = [k for k in CACHE if k[0] == file_id]

    for k in keys_to_delete:
        del CACHE[k]

