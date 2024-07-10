from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.libs.constants import MODULE_TYPE_NOT_FOUND
from app.libs.utils import generate_id, list_data, now
from app.models.modules import ModuleTypeModel
from app.routers.admin.schemas import ModuleTypeAdd


def get_module_types(
    db: Session,
    start: int,
    limit: int,
    sort_by: Optional[str] = None,
    order: Optional[str] = None,
    search: Optional[str] = None,
):
    data = list_data(
        db,
        model=ModuleTypeModel,
        start=start,
        limit=limit,
        sort_by=sort_by,
        order=order,
        search=search,
    )
    return data


def get_module_type(db: Session, module_type_id: str):
    module_type = (
        db.query(ModuleTypeModel).filter_by(id=module_type_id, is_deleted=False).first()
    )
    if not module_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=MODULE_TYPE_NOT_FOUND
        )
    return module_type


def add_module_type(db: Session, request: ModuleTypeAdd):
    # Add the module type
    module_type = ModuleTypeModel(id=generate_id(), **request.dict())
    db.add(module_type)
    db.commit()
    db.refresh(module_type)
    return module_type


def update_module_type(db: Session, module_type_id: str, request: ModuleTypeAdd):
    # Fetch the module type
    module_type = get_module_type(db, module_type_id)

    # Update the module type
    module_type.name = request.name
    module_type.update_at = now()
    db.commit()
    db.refresh(module_type)
    return module_type


def delete_module_type(db: Session, module_type_id: str):
    # Fetch the module type
    module_type = get_module_type(db, module_type_id)

    # Delete the module type
    module_type.is_deleted = True
    db.commit()
    db.refresh(module_type)
    return module_type
