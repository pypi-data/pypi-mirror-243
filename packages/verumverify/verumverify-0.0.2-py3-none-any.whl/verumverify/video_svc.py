import hashlib


def compute_hash_from_path(file_path, buffer_size=8192):
    sha256_hash = hashlib.sha256()
    with open(file_path, 'rb') as raw:
        for chunk in iter(lambda: raw.read(buffer_size), b''):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()
