import base64


def to_serializable(obj):
    # Jce解析需要递归解析

    if isinstance(obj, bytearray):
        return obj.hex()
    if isinstance(obj, dict):
        return {key: to_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [to_serializable(element) for element in obj]
    elif hasattr(obj, '__dict__'):
        return {key: to_serializable(value) for key, value in obj.__dict__.items()}
    else:
        return obj  # 基本类型
