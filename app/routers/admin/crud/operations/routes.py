from typing import List

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.routers.admin.crud.admin_users import admin_users
from app.routers.admin.crud.operations import operations
from app.routers.admin.schemas import RoleOperation

router = APIRouter(
    prefix="/operations",
    tags=["Operations"],
)


@router.get("")
def get_my_operation(token: str = Header(None), db: Session = Depends(get_db)):
    db_admin_user = admin_users.verify_token(db, token=token)
    data = operations.get_user_operation(db, admin_user_id=db_admin_user.id)
    return data


@router.get("/all", response_model=List[RoleOperation])
def get_all_operations(token: str = Header(None), db: Session = Depends(get_db)):
    admin_users.verify_token(db, token=token)
    data = operations.get_all_operations(db)
    return data
