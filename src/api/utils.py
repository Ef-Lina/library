from fastapi import Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordBearer

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.get("/test-auth")
def show_access_token(token: str = Depends(oauth2_scheme)):
    return {"token": token}
