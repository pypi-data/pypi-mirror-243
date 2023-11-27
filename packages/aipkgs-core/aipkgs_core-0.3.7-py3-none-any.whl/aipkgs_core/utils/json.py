def json_has_key(json: dict, key: str) -> bool:
    if key in json:
        return True
    return False


def json_key_value_is(json: dict, key: str, value: str) -> bool:
    if json_has_key(json=json, key=key):
        v = json[key]
        if value == v:
            return True
        else:
            return False
    else:
        raise Exception(f"provided json does not have key: {key}")


def json_key_value_contains(json: dict, key: str, content: str, sensitive: bool = None) -> bool:
    if json_has_key(json=json, key=key):
        v = json[key]
        v = v if sensitive else v.lower()
        content = content if sensitive else content.lower()
        if content in v:
            return True
        else:
            return False
    else:
        raise Exception(f"provided json does not have key: {key}")
