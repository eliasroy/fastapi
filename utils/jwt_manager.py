from jwt import encode,decode

def create_token(data:dict):
    token:str =encode(payload=data,key="secret",algorithm="HS256")
    return token

def validacion(token:str)->dict:
    data:dict= decode(token,key="secret",algorithms=['HS256'])
    return data