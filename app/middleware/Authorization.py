from typing import Tuple
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import requests 
import os

class Authorization:
    def __init__(self):
        self.security = HTTPBearer() 
        self.CORE_API_URL = os.getenv("CORE_API_URL")
        
    def __call__(self, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> Tuple[dict, str]:
        """
        Middleware que valida o usuário autenticado via Core API.
        """
        token = f"{credentials.scheme} {credentials.credentials}"

        try:
            response = requests.get(
                self.CORE_API_URL,
                headers={"Authorization": token}
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication credentials",
                )

            user_data = response.json()
            return user_data, token

        except requests.RequestException as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Failed to validate authentication credentials",
            ) from exc
