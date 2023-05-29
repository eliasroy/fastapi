
from fastapi import Request,HTTPException
from utils.jwt_manager   import create_token,validacion
from fastapi.security import HTTPBearer


class JWTBearer(HTTPBearer):
  async  def __call__(self, requests: Request) :
        auth= await super().__call__(requests)
        data=validacion(auth.credentials)
        if data['email']!='admin@gmail.com':
            raise HTTPException(status_code=403,detail="Credenciales invalidas")
