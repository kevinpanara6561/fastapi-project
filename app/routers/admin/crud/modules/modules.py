from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.libs.constants import (
    MODULE_NOT_FOUND,
    MODULE_TYPE_NOT_FOUND,
    PROJECT_NOT_FOUND,
)
from app.libs.utils import generate_id, list_data, now
from app.models.modules import ModuleModel
from app.routers.admin.crud.module_types.module_types import get_module_type
from app.routers.admin.crud.projects.projects import get_project
from app.routers.admin.schemas import ModuleAdd


def get_modules(
    db: Session,
    start: int,
    limit: int,
    sort_by: Optional[str] = None,
    order: Optional[str] = None,
    search: Optional[str] = None,
):
    data = list_data(
        db,
        model=ModuleModel,
        start=start,
        limit=limit,
        sort_by=sort_by,
        order=order,
        search=search,
    )
    return data


def get_module(db: Session, module_id: str):
    module = db.query(ModuleModel).filter_by(id=module_id, is_deleted=False).first()
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=MODULE_NOT_FOUND
        )
    return module


def check_project_and_module_type(db: Session, project_id: str, module_type_id: str):
    # Fetch the project
    project = get_project(db, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=PROJECT_NOT_FOUND
        )

    # Fetch the module type
    module_type = get_module_type(db, module_type_id)
    if not module_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=MODULE_TYPE_NOT_FOUND
        )


def add_module(db: Session, request: ModuleAdd):
    # Check if the project and module type exists
    check_project_and_module_type(db, request.project_id, request.module_type_id)

    # Add the module
    module = ModuleModel(id=generate_id(), **request.dict())
    db.add(module)
    db.commit()
    db.refresh(module)
    return module


def update_module(db: Session, module_id: str, request: ModuleAdd):
    # Check if the project and module type exists
    check_project_and_module_type(db, request.project_id, request.module_type_id)

    # Fetch the module
    module = get_module(db, module_id)

    # Update the module
    module.name = request.name
    module.description = request.description
    module.project_id = request.project_id
    module.module_type_id = request.module_type_id
    module.update_at = now()

    db.commit()
    db.refresh(module)
    return module


def delete_module(db: Session, module_id: str):
    # Fetch the module
    module = get_module(db, module_id)

    # Delete the module
    module.is_deleted = True
    db.commit()
    db.refresh(module)
    return module
