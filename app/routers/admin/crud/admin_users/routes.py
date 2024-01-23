from typing import List, Optional

from fastapi import APIRouter, Depends, Header, Path, Query, Response, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.libs.constants import ADMIN_USER_ID, ORDER_BY
from app.routers.admin.crud.admin_users import admin_users
from app.routers.admin.crud.operations import operations
from app.routers.admin.schemas import (
    AdminUser,
    AdminUserAdd,
    AdminUserAll,
    AdminUserList,
    AdminUserResetPassword,
    AdminUserSmall,
    AdminUserUpdate,
)

router = APIRouter(prefix="/admin-users", tags=["Admin Users"])


@router.get("", response_model=AdminUserList)
def get_admin_users(
    token: str = Header(None),
    start: int = 0,
    limit: int = 10,
    sort_by: Optional[str] = Query(None, max_length=50),
    order: Optional[str] = Query(None, max_length=4, description=ORDER_BY),
    search: Optional[str] = Query(None, max_length=50),
    db: Session = Depends(get_db),
):
    db_admin_user = admin_users.verify_token(db, token=token)
    operations.verify_admin_user_operation(
        db, admin_user_id=db_admin_user.id, operation="List Admin Users"
    )
    data = admin_users.get_admin_users(
        db, start=start, limit=limit, sort_by=sort_by, order=order, search=search
    )
    return data


@router.post("", status_code=status.HTTP_201_CREATED)
def add_admin_user(
    admin_user: AdminUserAdd,
    token: str = Header(None),
    db: Session = Depends(get_db),
):
    db_admin_user = admin_users.verify_token(db, token=token)
    operations.verify_admin_user_operation(
        db, admin_user_id=db_admin_user.id, operation="Add Admin User"
    )
    data = admin_users.add_admin_user(db, admin_user=admin_user)
    return data


@router.get(
    "/all",
    response_model=List[AdminUserSmall],
    tags=["Admin Users"],
)
def get_all_admin_users(token: str = Header(None), db: Session = Depends(get_db)):
    admin_users.verify_token(db, token=token)
    data = admin_users.get_all_admin_users(db)
    return data


@router.get(
    "/{admin_user_id}",
    response_model=AdminUserAll,
    tags=["Admin Users"],
)
def get_admin_user(
    token: str = Header(None),
    admin_user_id: str = Path(title=ADMIN_USER_ID, min_length=36, max_length=36),
    db: Session = Depends(get_db),
):
    db_admin_user = admin_users.verify_token(db, token=token)
    operations.verify_admin_user_operation(
        db, admin_user_id=db_admin_user.id, operation="Edit Admin User"
    )
    data = admin_users.get_admin_user(db, admin_user_id=admin_user_id)
    return data


@router.put(
    "/{admin_user_id}",
    response_model=AdminUser,
    tags=["Admin Users"],
)
def update_admin_user(
    admin_user: AdminUserUpdate,
    token: str = Header(None),
    admin_user_id: str = Path(title=ADMIN_USER_ID, min_length=36, max_length=36),
    db: Session = Depends(get_db),
):
    db_admin_user = admin_users.verify_token(db, token=token)
    operations.verify_admin_user_operation(
        db, admin_user_id=db_admin_user.id, operation="Edit Admin User"
    )
    data = admin_users.update_admin_user(
        db, admin_user_id=admin_user_id, admin_user=admin_user
    )
    return data


@router.delete(
    "/{admin_user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Admin Users"],
)
def delete_admin_user(
    token: str = Header(None),
    admin_user_id: str = Path(title=ADMIN_USER_ID, min_length=36, max_length=36),
    db: Session = Depends(get_db),
):
    db_admin_user = admin_users.verify_token(db, token=token)
    operations.verify_admin_user_operation(
        db, admin_user_id=db_admin_user.id, operation="Delete Admin User"
    )
    admin_users.delete_admin_user(db, admin_user_id=admin_user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put(
    "/{admin_user_id}/reset-password",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Admin Users"],
)
def reset_password(
    admin_user: AdminUserResetPassword,
    token: str = Header(None),
    admin_user_id: str = Path(title=ADMIN_USER_ID, min_length=36, max_length=36),
    db: Session = Depends(get_db)
):
    db_admin_user = admin_users.verify_token(db, token=token)
    operations.verify_admin_user_operation(
        db, admin_user_id=db_admin_user.id, operation="Reset Password"
    )
    admin_users.reset_password(db, admin_user=admin_user, admin_user_id=admin_user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
