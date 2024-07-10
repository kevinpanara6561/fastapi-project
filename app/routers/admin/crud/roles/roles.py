from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.libs.constants import ROLE_NOT_FOUND
from app.libs.utils import generate_id, now
from app.models.auth import OperationModel, RoleModel, RoleOperationModel
from app.routers.admin.crud.operations.operations import get_operation
from app.routers.admin.schemas import OperationMaster, RoleAdd


def get_roles(
    db: Session,
    start: int,
    limit: int,
    sort_by: Optional[str] = None,
    order: Optional[str] = None,
    search: Optional[str] = None,
):
    query = db.query(RoleModel).filter(RoleModel.is_deleted == False)

    if search:
        text = f"""%{search}%"""
        query = query.filter(RoleModel.name.like(text))

    if sort_by == "name":
        if order == "desc":
            query = query.order_by(RoleModel.name.desc())
        else:
            query = query.order_by(RoleModel.name)
    else:
        query = query.order_by(RoleModel.updated_at.desc())

    results = query.offset(start).limit(limit).all()
    count = query.count()
    data = {"count": count, "list": results}
    return data


def get_all_roles(db: Session):
    roles = (
        db.query(RoleModel)
        .filter(RoleModel.is_deleted == False, RoleModel.editable == True)
        .order_by(RoleModel.name)
        .all()
    )
    return roles


def get_role_by_name(db: Session, name: str):
    return (
        db.query(RoleModel)
        .filter(RoleModel.name == name, RoleModel.is_deleted == False)
        .first()
    )


def add_role_operations(db: Session, role_id: str, operations: List[str]):
    for operation in operations:
        db_operation = get_operation(db, operation_id=operation)
        if db_operation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Operation not found"
            )
        db_role_operation = RoleOperationModel(
            id=generate_id(), role_id=role_id, operation_id=operation
        )
        db.add(db_role_operation)
    db.commit()


def get_role_by_id(db: Session, role_id: str):
    return (
        db.query(RoleModel)
        .filter(RoleModel.id == role_id, RoleModel.is_deleted == False)
        .first()
    )


def get_role_details(db: Session, role_id: str):
    db_role = get_role_by_id(db=db, role_id=role_id)
    if db_role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ROLE_NOT_FOUND
        )

    db_role_operations = (
        db.query(OperationModel)
        .join(RoleOperationModel)
        .filter(RoleOperationModel.role_id == role_id)
        .all()
    )
    # Create instances of OperationMaster and populate the operations list
    operations = [
        OperationMaster(id=operation.id, name=operation.slug)
        for operation in db_role_operations
    ]
    db_role.operations = operations
    return db_role


def get_role(db: Session, role_id: str) -> RoleModel:
    db_role = get_role_by_id(db, role_id=role_id)
    if db_role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ROLE_NOT_FOUND
        )
    return db_role


def add_role(db: Session, role: RoleAdd) -> RoleModel:
    name = role.name
    db_role = get_role_by_name(db, name=name)
    if db_role:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Role already exist."
        )
    db_role = RoleModel(id=generate_id(), slug=name, name=name)
    db.add(db_role)
    add_role_operations(db, role_id=db_role.id, operations=role.operations)
    db.commit()
    return get_role_details(db=db, role_id=db_role.id)


def delete_role_operations(db: Session, role_id: str):
    db.query(RoleOperationModel).filter(RoleOperationModel.role_id == role_id).delete()


def update_role(db: Session, role_id: str, role: RoleAdd):
    name = role.name
    db_role = get_role(db, role_id=role_id)
    if db_role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ROLE_NOT_FOUND
        )

    if db_role.editable == False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    if db_role.name.lower() != name.lower():
        _db_role = get_role_by_name(db, name=name)
        if _db_role:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Role already exist."
            )
    db_role.name = name
    delete_role_operations(db, role_id=role_id)
    add_role_operations(db, role_id=role_id, operations=role.operations)
    db.commit()


def delete_role(db: Session, role_id: str):
    db_role = get_role(db, role_id=role_id)
    if db_role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ROLE_NOT_FOUND
        )

    if db_role.editable == False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )

    db_role.is_deleted = True
    db_role.updated_at = now()
    db.commit()
