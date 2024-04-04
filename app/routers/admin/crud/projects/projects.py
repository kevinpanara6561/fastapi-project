from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.libs.constants import ADMIN_USER_NOT_FOUND, PROJECT_NOT_FOUND
from app.libs.utils import generate_id, list_data, now
from app.models import ProjectModel, ProjectUserModel
from app.routers.admin.crud.admin_users.admin_users import get_admin_user
from app.routers.admin.schemas import (
    ProjectAdd,
    ProjectStatusChange,
    ProjectUser,
    ProjectUserAssign,
)


def get_projects(
    db: Session,
    start: int,
    limit: int,
    sort_by: Optional[str] = None,
    order: Optional[str] = None,
    search: Optional[str] = None,
):
    data = list_data(
        db,
        model=ProjectModel,
        start=start,
        limit=limit,
        sort_by=sort_by,
        order=order,
        search=search,
    )
    return data


def get_project(db: Session, project_id: str):
    project = db.query(ProjectModel).filter_by(id=project_id, is_deleted=False).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=PROJECT_NOT_FOUND
        )
    return project


def get_project_by_name(db: Session, name: str):
    return (
        db.query(ProjectModel)
        .filter(ProjectModel.name == name, ProjectModel.is_deleted == False)
        .first()
    )


def add_project(db: Session, request: ProjectAdd):
    # Check if the project already exists
    project = get_project_by_name(db, request.name)
    if project:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Project already exists."
        )

    # Check if the manager exists
    user = get_admin_user(db, request.manager_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ADMIN_USER_NOT_FOUND
        )

    # Add the project
    project = ProjectModel(id=generate_id(), **request.dict())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def update_project(db: Session, project_id: str, request: ProjectAdd):
    # Check if the manager exists
    user = get_admin_user(db, request.manager_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ADMIN_USER_NOT_FOUND
        )

    # Fetch the project
    project = get_project(db, project_id)

    # Update the project
    project.name = request.name
    project.description = request.description
    project.start_date = request.start_date
    project.end_date = request.end_date
    project.manager_id = request.manager_id
    project.updated_at = now()

    db.commit()
    db.refresh(project)
    return project
            

def delete_project(db: Session, project_id: str):
    # Fetch the project
    project = get_project(db, project_id)

    # Delete the project
    project.is_deleted = True
    db.commit()
    db.refresh(project)
    return project


def change_status(db: Session, request: ProjectStatusChange):
    # Fetch the project
    project = get_project(db, request.project_id)

    # Change the status
    project.status = request.status
    db.commit()


def assign_user(db: Session, request: ProjectUserAssign) -> ProjectUser:
    # Iterate through the list of admin_user_ids in the request
    for admin_user_id in request.admin_user_ids:
        id = generate_id()
        project_user = ProjectUserModel(
            id=id, project_id=request.project_id, admin_user_id=admin_user_id
        )
        db.add(project_user)
        db.commit()
        db.refresh(project_user)

    # Retrieve the admin_users based on their ids and create a list
    admin_users = [
        get_admin_user(db, admin_user_id) for admin_user_id in request.admin_user_ids
    ]

    # Set the admin_users list to the project_user instance
    project_user.admin_users = admin_users
    return project_user


def remove_user(db: Session, request: ProjectUserAssign):
    for admin_user_id in request.admin_user_ids:
        project_user = (
            db.query(ProjectUserModel)
            .filter_by(project_id=request.project_id, admin_user_id=admin_user_id)
            .first()
        )
        db.delete(project_user)
        db.commit()
