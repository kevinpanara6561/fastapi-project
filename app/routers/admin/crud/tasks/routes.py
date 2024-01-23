from typing import Optional

from fastapi import APIRouter, Depends, Header, Path, Query, Response, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.libs.constants import ORDER_BY, TASK_ID
from app.routers.admin.crud.admin_users import admin_users
from app.routers.admin.crud.operations import operations
from app.routers.admin.crud.tasks import tasks
from app.routers.admin.schemas import Task, TaskAdd, TaskList, TaskStatusChange

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("", response_model=TaskList)
def get_tasks(
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
    data = tasks.get_tasks(
        db, start=start, limit=limit, sort_by=sort_by, order=order, search=search
    )
    return data


@router.get("/{task_id}", response_model=Task)
def get_task(
    token: str = Header(None),
    task_id: str = Path(title=TASK_ID, min_length=36, max_length=36),
    db: Session = Depends(get_db),
):
    db_admin_user = admin_users.verify_token(db, token=token)
    # operations.verify_admin_user_operation(
    #     db, admin_user_id=db_admin_user.id, operation="Edit Admin User"
    # )
    data = tasks.get_task(db, task_id=task_id)
    return data


@router.post("", status_code=status.HTTP_201_CREATED, response_model=Task)
def add_task(
    request: TaskAdd,
    token: str = Header(None),
    db: Session = Depends(get_db),
):
    db_admin_user = admin_users.verify_token(db, token=token)
    # operations.verify_admin_user_operation(
    #     db, admin_user_id=db_admin_user.id, operation="Add Admin User"
    # )
    data = tasks.add_task(db, request=request)
    return data


@router.put("/{task_id}", response_model=Task)
def update_task(
    request: TaskAdd,
    token: str = Header(None),
    task_id: str = Path(title=TASK_ID, min_length=36, max_length=36),
    db: Session = Depends(get_db),
):
    db_admin_user = admin_users.verify_token(db, token=token)
    # operations.verify_admin_user_operation(
    #     db, admin_user_id=db_admin_user.id, operation="Edit Admin User"
    # )
    data = tasks.update_task(db, task_id=task_id, request=request)
    return data


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    token: str = Header(None),
    task_id: str = Path(title=TASK_ID, min_length=36, max_length=36),
    db: Session = Depends(get_db),
):
    db_admin_user = admin_users.verify_token(db, token=token)
    # operations.verify_admin_user_operation(
    #     db, admin_user_id=db_admin_user.id, operation="Delete Admin User"
    # )
    tasks.delete_task(db, task_id=task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{task_id}/status")
def change_status(
    request: TaskStatusChange,
    token: str = Header(None),
    db: Session = Depends(get_db),
):
    db_admin_user = admin_users.verify_token(db, token=token)
    # operations.verify_admin_user_operation(
    #     db, admin_user_id=db_admin_user.id, operation="Edit Admin User"
    # )
    tasks.change_status(db, request=request)
    return f"Task Status Changed to {request.status.name}"
