import enum
import json


class FileAccessLevelEnum(enum.Enum):
    write = "w+"
    read = "r"


def create_file(name: str, content: str, access: FileAccessLevelEnum):
    file = open_file(name=name, access=access)
    file.write(content)


def open_file(name: str, access: FileAccessLevelEnum):
    file = open(name, access.value)
    return file


def close_file(file):
    file.close()


def open_json_file(path: str):
    with open(path) as f:
        return json.load(f)


def read_from_json_file(path: str, key: str, default: str = None):
    content_dict: dict = open_json_file(path=path)
    if key in content_dict:
        return content_dict[key]
    else:
        return default or key


