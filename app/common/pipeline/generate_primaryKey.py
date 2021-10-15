from app.common.helpers.helper import keyGenerate


def generate_primaryKey(length: int = None):
    s = []
    if length is not None:
        for i in range(length):
            s.append(keyGenerate(keyLen=6, case='lower'))
    return s
