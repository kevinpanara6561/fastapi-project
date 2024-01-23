from typing import Optional

from fastapi import APIRouter, Depends, Header, Path, Query, Response, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.libs.constants import MODULE_ID, ORDER_BY
from app.routers.admin.crud.admin_users import admin_users
from app.routers.admin.crud.modules import modules
from app.routers.admin.crud.operations import operations
from app.routers.admin.schemas import Module, ModuleAdd, ModuleList

router = APIRouter(prefix="/modules", tags=["Modules"])


@router.get("", response_model=ModuleList)
def get_modules(
    token: str = Header(None),
    start: int = 0,
    limit: int = 10,
    sort_by: Optional[str] = Query(None, max_length=50),
    order: Optional[str] = Query(None, max_length=4, description=ORDER_BY),
    search: Optional[str] = Query(None, max_length=50),
    db: Session = Depends(get_db),
):
    db_admin_user = admin_users.verify_token(db, token=token)
    # operations.verify_admin_user_operation(
    #     db, admin_user_id=db_admin_user.id, operation="List Admin Users"
    # )
    data = modules.get_modules(
        db, start=start, limit=limit, sort_by=sort_by, order=order, search=search
    )
    return data


@router.get("/{module_id}", response_model=Module)
def get_module(
    token: str = Header(None),
    module_id: str = Path(title=MODULE_ID, min_length=36, max_length=36),
    db: Session = Depends(get_db),
):
    db_admin_user = admin_users.verify_token(db, token=token)
    # operations.verify_admin_user_operation(
    #     db, admin_user_id=db_admin_user.id, operation="Edit Admin User"
    # )
    data = modules.get_module(db, module_id=module_id)
    return data


@router.post("", status_code=status.HTTP_201_CREATED, response_model=Module)
def add_module(
    request: ModuleAdd,
    token: str = Header(None),
    db: Session = Depends(get_db),
):
    db_admin_user = admin_users.verify_token(db, token=token)
    # operations.verify_admin_user_operation(
    #     db, admin_user_id=db_admin_user.id, operation="Add Admin User"
    # )
    data = modules.add_module(db, request=request)
    return data


@router.put("/{module_id}", response_model=Module)
def update_module(
    request: ModuleAdd,
    token: str = Header(None),
    module_id: str = Path(title=MODULE_ID, min_length=36, max_length=36),
    db: Session = Depends(get_db),
):
    db_admin_user = admin_users.verify_token(db, token=token)
    # operations.verify_admin_user_operation(
    #     db, admin_user_id=db_admin_user.id, operation="Edit Admin User"
    # )
    data = modules.update_module(db, module_id=module_id, request=request)
    return data


@router.delete("/{module_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_module(
    token: str = Header(None),
    module_id: str = Path(title=MODULE_ID, min_length=36, max_length=36),
    db: Session = Depends(get_db),
):
    db_admin_user = admin_users.verify_token(db, token=token)
    # operations.verify_admin_user_operation(
    #     db, admin_user_id=db_admin_user.id, operation="Delete Admin User"
    # )
    modules.delete_module(db, module_id=module_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
