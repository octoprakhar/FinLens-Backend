STATUS_STORE = {}

def set_status(file_id: str, status: str):
    STATUS_STORE[file_id] = status

def get_status(file_id: str):
    return STATUS_STORE.get(file_id,"not_found")
