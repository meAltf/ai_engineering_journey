import uuid

# id = str(uuid.uuid5(uuid.NAMESPACE_DNS, key))

def seconds_to_timestamp(seconds: int):
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins:02d}:{secs:02d}"