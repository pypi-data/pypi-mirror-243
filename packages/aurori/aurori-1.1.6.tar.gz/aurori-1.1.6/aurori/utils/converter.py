def unicode_string_to_bytes(string):
    if isinstance(string, str):
        bytes_object = bytes(string, 'utf-8')
    else:
        bytes_object = string
    return bytes_object