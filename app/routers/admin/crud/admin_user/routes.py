from fastapi import APIRouter, Depends, Header, Response, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.routers.admin.crud.admin_users import admin_users
from app.routers.admin.schemas import (
    AdminUserChangePassword,
    AdminUserProfileUpdate,
    MyProfile,
)

router = APIRouter(prefix="/admin-user", tags=["Admin User"])


@router.get("", response_model=MyProfile)
def get_my_profile(token: str = Header(None), db: Session = Depends(get_db)):
    data = admin_users.verify_token(db, token=token)
    return data


@router.put("", response_model=MyProfile)
def update_profile(
    admin_user: AdminUserProfileUpdate,
    token: str = Header(None),
    db: Session = Depends(get_db),
):
    data = admin_users.update_profile(db, admin_user=admin_user, token=token)
    return data


@router.put(
    "/change-password",
    status_code=status.HTTP_204_NO_CONTENT,
)
def change_password(
    admin_user: AdminUserChangePassword,
    token: str = Header(None),
    db: Session = Depends(get_db),
):
    admin_users.verify_token(db, token=token)
    admin_users.change_password(db, admin_user=admin_user, token=token)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
