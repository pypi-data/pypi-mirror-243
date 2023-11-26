import emoji
import re


# region emoji
def is_emoji(s):
    for lang in emoji.UNICODE_EMOJI_ENGLISH:
        if s in emoji.UNICODE_EMOJI_ENGLISH[lang]: return True
    return False


def contains_emoji(txt: str):
    for c in txt:
        if is_emoji(c):
            return True
    return False


def contains_special_characters(txt: str):
    special_characters = "!@#$%^&*"
    count = 0
    for sc in special_characters:
        count += txt.count(sc)
        if count > 1:
            return True
    return bool(count)


def contains_mal_phrases(txt: str):
    phrases = ['sex', 'porn']
    count = 0
    for sc in phrases:
        count += txt.count(sc)
        if count > 1:
            return True
    return bool(count)


def is_validate(txt: str):
    if contains_emoji(txt=txt) or contains_special_characters(txt=txt) or contains_mal_phrases(txt=txt):
        return False
    return True
# endregion


# region regex
def validate_regex(regex: str, txt: str) -> bool:
    pattern = re.compile(regex)
    if re.match(regex, txt):
        return True
    else:
        return False
# endregion
