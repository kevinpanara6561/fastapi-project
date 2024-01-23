from typing import List, Optional

from fastapi import APIRouter, Depends, Header, Path, Query, Response, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.libs.constants import ORDER_BY, ROLE_ID
from app.routers.admin.crud.admin_users import admin_users
from app.routers.admin.crud.operations import operations
from app.routers.admin.crud.roles import roles
from app.routers.admin.schemas import Role, RoleAdd, RoleDetails, RoleList

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get("", response_model=RoleList)
def get_roles(
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
        db, admin_user_id=db_admin_user.id, operation="List Roles"
    )
    data = roles.get_roles(
        db, start=start, limit=limit, sort_by=sort_by, order=order, search=search
    )
    return data


@router.post(
    "",
    response_model=RoleDetails,
    status_code=status.HTTP_201_CREATED,
)
def add_role(role: RoleAdd, token: str = Header(None), db: Session = Depends(get_db)):
    db_admin_user = admin_users.verify_token(db, token=token)
    operations.verify_admin_user_operation(
        db, admin_user_id=db_admin_user.id, operation="Add Role"
    )
    data = roles.add_role(db, role=role)
    return data


@router.get("/all", response_model=List[Role])
def get_all_roles(token: str = Header(None), db: Session = Depends(get_db)):
    admin_users.verify_token(db, token=token)
    data = roles.get_all_roles(db)
    return data


@router.get("/{role_id}", response_model=RoleDetails)
def get_role(
    role_id: str = Path(title=ROLE_ID, min_length=36, max_length=36),
    token: str = Header(None),
    db: Session = Depends(get_db),
):
    db_admin_user = admin_users.verify_token(db, token=token)
    operations.verify_admin_user_operation(
        db, admin_user_id=db_admin_user.id, operation="Edit Role"
    )
    data = roles.get_role_details(db, role_id=role_id)
    return data


@router.put("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_role(
    role: RoleAdd,
    token: str = Header(None),
    role_id: str = Path(title=ROLE_ID, min_length=36, max_length=36),
    db: Session = Depends(get_db),
):
    db_admin_user = admin_users.verify_token(db, token=token)
    operations.verify_admin_user_operation(
        db, admin_user_id=db_admin_user.id, operation="Edit Role"
    )
    roles.update_role(db, role_id=role_id, role=role)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(
    token: str = Header(None),
    role_id: str = Path(title=ROLE_ID, min_length=36, max_length=36),
    db: Session = Depends(get_db),
):
    db_admin_user = admin_users.verify_token(db, token=token)
    operations.verify_admin_user_operation(
        db, admin_user_id=db_admin_user.id, operation="Delete Role"
    )
    roles.delete_role(db, role_id=role_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
