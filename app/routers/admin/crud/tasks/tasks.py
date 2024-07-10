from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.libs.constants import MODULE_NOT_FOUND, TASK_NOT_FOUND
from app.libs.utils import generate_id, list_data
from app.models.tasks import TaskModel
from app.routers.admin.crud.module_types.module_types import get_module_type
from app.routers.admin.crud.modules.modules import get_module
from app.routers.admin.crud.projects.projects import get_project
from app.routers.admin.schemas import TaskAdd, TaskStatusChange


def get_tasks(
    db: Session,
    start: int,
    limit: int,
    sort_by: Optional[str] = None,
    order: Optional[str] = None,
    search: Optional[str] = None,
):
    data = list_data(
        db,
        model=TaskModel,
        start=start,
        limit=limit,
        sort_by=sort_by,
        order=order,
        search=search,
    )
    return data


def get_task(db: Session, task_id: str):
    task = db.query(TaskModel).filter_by(id=task_id, is_deleted=False).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=TASK_NOT_FOUND
        )
    return task


def add_task(db: Session, request: TaskAdd):
    # Check if module is exists
    module = get_module(db, request.module_id)
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=MODULE_NOT_FOUND
        )

    # Add the task
    task = TaskModel(id=generate_id(), **request.dict())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task(db: Session, task_id: str, request: TaskAdd):
    # Fetch the task
    task = get_task(db, task_id)

    # Check if module is exists
    module = get_module(db, request.module_id)
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=MODULE_NOT_FOUND
        )

    # Update the task
    task.name = request.name
    task.description = request.description
    task.module_id = request.module_id

    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: str):
    # Fetch the task
    task = get_task(db, task_id)

    # Delete the task
    task.is_deleted = True
    db.commit()


def change_status(db: Session, request: TaskStatusChange):
    # Fetch the task
    task = get_task(db, request.task_id)

    # Change the status
    task.status = request.status
    db.commit()
