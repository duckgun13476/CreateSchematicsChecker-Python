import json
from nbt import nbt



def nbt_int(nbt_123):
    return int(str(nbt_123))

def safe_get_array(item,pos:str):
    if isinstance(item, nbt.TAG_Int_Array):
        X,Y,Z = json.loads(str(item))
    else:
        X = nbt_int(item.get('X'))
        Y = nbt_int(item.get('Y'))
        Z = nbt_int(item.get('Z'))

    if pos == 'X':
        return int(X)
    elif pos == 'Y':
        return int(Y)
    elif pos == 'Z':
        return int(Z)
    else:
        return None