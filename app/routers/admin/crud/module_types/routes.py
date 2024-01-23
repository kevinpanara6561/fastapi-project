from typing import Optional

from fastapi import APIRouter, Depends, Header, Path, Query, Response, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.libs.constants import MODULE_TYPE_ID, ORDER_BY
from app.routers.admin.crud.admin_users import admin_users
from app.routers.admin.crud.module_types import module_types
from app.routers.admin.crud.operations import operations
from app.routers.admin.schemas import ModuleType, ModuleTypeAdd, ModuleTypeList

router = APIRouter(prefix="/module-types", tags=["Module Types"])


@router.get("", response_model=ModuleTypeList)
def get_module_types(
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
    data = module_types.get_module_types(
        db, start=start, limit=limit, sort_by=sort_by, order=order, search=search
    )
    return data


@router.get("/{module_type_id}", response_model=ModuleType)
def get_module_type(
    token: str = Header(None),
    module_type_id: str = Path(title=MODULE_TYPE_ID, min_length=36, max_length=36),
    db: Session = Depends(get_db),
):
    db_admin_user = admin_users.verify_token(db, token=token)
    # operations.verify_admin_user_operation(
    #     db, admin_user_id=db_admin_user.id, operation="Edit Admin User"
    # )
    data = module_types.get_module_type(db, module_type_id=module_type_id)
    return data


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ModuleType)
def add_module_type(
    request: ModuleTypeAdd,
    token: str = Header(None),
    db: Session = Depends(get_db),
):
    db_admin_user = admin_users.verify_token(db, token=token)
    # operations.verify_admin_user_operation(
    #     db, admin_user_id=db_admin_user.id, operation="Add Admin User"
    # )
    data = module_types.add_module_type(db, request=request)
    return data


@router.put("/{module_type_id}", response_model=ModuleType)
def update_module_type(
    request: ModuleTypeAdd,
    token: str = Header(None),
    module_type_id: str = Path(title=MODULE_TYPE_ID, min_length=36, max_length=36),
    db: Session = Depends(get_db),
):
    db_admin_user = admin_users.verify_token(db, token=token)
    # operations.verify_admin_user_operation(
    #     db, admin_user_id=db_admin_user.id, operation="Edit Admin User"
    # )
    data = module_types.update_module_type(
        db, module_type_id=module_type_id, request=request
    )
    return data


@router.delete("/{module_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_module_type(
    token: str = Header(None),
    module_type_id: str = Path(title=MODULE_TYPE_ID, min_length=36, max_length=36),
    db: Session = Depends(get_db),
):
    db_admin_user = admin_users.verify_token(db, token=token)
    # operations.verify_admin_user_operation(
    #     db, admin_user_id=db_admin_user.id, operation="Delete Admin User"
    # )
    module_types.delete_module_type(db, module_type_id=module_type_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
