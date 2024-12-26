from typing import List
from fastapi import Depends, HTTPException, status

from user.models import User
from user.authentication import get_current_active_user

def role_checker_factory(allowed_roles: List[str]):
    def role_checker(user: User = Depends(get_current_active_user)):
        if user.role.role in allowed_roles:
            return True
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You don't have enough permissions"
        )
    return role_checker
