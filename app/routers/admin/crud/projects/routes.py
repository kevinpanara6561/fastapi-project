from typing import Optional

from fastapi import APIRouter, Depends, Header, Path, Query, Response, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.libs.constants import ORDER_BY, PROJECT_ID
from app.routers.admin.crud.admin_users import admin_users
from app.routers.admin.crud.operations import operations
from app.routers.admin.crud.projects import projects
from app.routers.admin.schemas import (
    Project,
    ProjectAdd,
    ProjectList,
    ProjectStatusChange,
    ProjectUser,
    ProjectUserAssign,
)

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("", response_model=ProjectList)
def get_projects(
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
    data = projects.get_projects(
        db, start=start, limit=limit, sort_by=sort_by, order=order, search=search
    )
    return data


@router.get("/{project_id}", response_model=Project)
def get_project(
    token: str = Header(None),
    project_id: str = Path(title=PROJECT_ID, min_length=36, max_length=36),
    db: Session = Depends(get_db),
):
    db_admin_user = admin_users.verify_token(db, token=token)
    # operations.verify_admin_user_operation(
    #     db, admin_user_id=db_admin_user.id, operation="Edit Admin User"
    # )
    data = projects.get_project(db, project_id=project_id)
    return data


@router.post("", status_code=status.HTTP_201_CREATED, response_model=Project)
def add_project(
    request: ProjectAdd,
    token: str = Header(None),
    db: Session = Depends(get_db),
):
    db_admin_user = admin_users.verify_token(db, token=token)
    # operations.verify_admin_user_operation(
    #     db, admin_user_id=db_admin_user.id, operation="Add Admin User"
    # )
    data = projects.add_project(db, request=request)
    return data


@router.put("/{project_id}", response_model=Project)
def update_project(
    request: ProjectAdd,
    token: str = Header(None),
    project_id: str = Path(title=PROJECT_ID, min_length=36, max_length=36),
    db: Session = Depends(get_db),
):
    db_admin_user = admin_users.verify_token(db, token=token)
    # operations.verify_admin_user_operation(
    #     db, admin_user_id=db_admin_user.id, operation="Edit Admin User"
    # )
    data = projects.update_project(db, project_id=project_id, request=request)
    return data


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    token: str = Header(None),
    project_id: str = Path(title=PROJECT_ID, min_length=36, max_length=36),
    db: Session = Depends(get_db),
):
    db_admin_user = admin_users.verify_token(db, token=token)
    # operations.verify_admin_user_operation(
    #     db, admin_user_id=db_admin_user.id, operation="Delete Admin User"
    # )
    projects.delete_project(db, project_id=project_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{project_id}/status")
def change_status(
    request: ProjectStatusChange,
    token: str = Header(None),
    db: Session = Depends(get_db),
):
    db_admin_user = admin_users.verify_token(db, token=token)
    # operations.verify_admin_user_operation(
    #     db, admin_user_id=db_admin_user.id, operation="Edit Admin User"
    # )
    projects.change_status(db, request=request)
    return f"Project Status Changed to {request.status.name}"


@router.post(
    "/assign_project", status_code=status.HTTP_201_CREATED, response_model=ProjectUser
)
def assign_user(
    request: ProjectUserAssign,
    token: str = Header(None),
    db: Session = Depends(get_db),
):
    db_admin_user = admin_users.verify_token(db, token=token)
    # operations.verify_admin_user_operation(
    #     db, admin_user_id=db_admin_user.id, operation="Add Admin User"
    # )
    data = projects.assign_user(db, request=request)
    return data


@router.delete("/remove_project")
def remove_user(
    request: ProjectUserAssign,
    token: str = Header(None),
    db: Session = Depends(get_db),
):
    db_admin_user = admin_users.verify_token(db, token=token)
    # operations.verify_admin_user_operation(
    #     db, admin_user_id=db_admin_user.id, operation="Add Admin User"
    # )
    projects.remove_user(db, request=request)
    return "User removed"
