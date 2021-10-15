import random
import string


def transcript_string_formation(transcript_arr: list) -> str:
    script = ""
    if len(transcript_arr) > 0:
        for i in transcript_arr:
            script = script + i["text"]
    return script


def keyGenerate(keyLen: int, case: str = 'upper') -> str:
    k = ""
    try:
        if isinstance(keyLen, int):
            if case is 'upper':
                k = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(keyLen))
            else:
                k = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(keyLen))
        return k
    except Exception as ex:
        return ex.__cause__
