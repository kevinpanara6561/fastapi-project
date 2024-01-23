from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.libs.constants import ISSUE_NOT_FOUND, TASK_NOT_FOUND
from app.libs.utils import generate_id, list_data, now
from app.models import IssueModel, IssueStatusEnum, IssueUserModel
from app.routers.admin.crud.admin_users.admin_users import get_admin_user
from app.routers.admin.crud.tasks.tasks import get_task
from app.routers.admin.schemas import IssueAdd, IssueUser, IssueUserAssign


def get_issues(
    db: Session,
    start: int,
    limit: int,
    sort_by: Optional[str] = None,
    order: Optional[str] = None,
    search: Optional[str] = None,
):
    data = list_data(
        db,
        model=IssueModel,
        start=start,
        limit=limit,
        sort_by=sort_by,
        order=order,
        search=search,
    )
    return data


def get_issue(db: Session, issue_id: str):
    issue = db.query(IssueModel).filter_by(id=issue_id, is_deleted=False).first()
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ISSUE_NOT_FOUND
        )
    return issue


def get_open_issue(db: Session, issue_id: str):
    issue = (
        db.query(IssueModel)
        .filter_by(id=issue_id, is_deleted=False, status=IssueStatusEnum.OPEN)
        .first()
    )
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ISSUE_NOT_FOUND
        )
    return issue


def add_issue(db: Session, request: IssueAdd):
    # Check if task is exists
    task = get_task(db, request.task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=TASK_NOT_FOUND
        )

    # Add the issue
    issue = IssueModel(id=generate_id(), **request.dict())
    db.add(issue)
    db.commit()
    db.refresh(issue)
    return issue


def update_issue(db: Session, issue_id: str, request: IssueAdd):
    # Fetch the issue
    issue = get_issue(db, issue_id)

    # Check if task is exists
    task = get_task(db, request.task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=TASK_NOT_FOUND
        )

    # Update the issue
    issue.name = request.name
    issue.description = request.description
    issue.task_id = request.task_id
    issue.update_at = now()

    db.commit()
    db.refresh(issue)
    return issue


def delete_issue(db: Session, issue_id: str):
    # Fetch the issue
    issue = get_issue(db, issue_id)

    # Delete the issue
    issue.is_deleted = True
    db.commit()


def close_issue(db: Session, issue_id: str):
    # Fetch the issue
    issue = get_open_issue(db, issue_id)

    # Close the issue
    issue.status = IssueStatusEnum.CLOSED
    db.commit()
    db.refresh(issue)
    return issue


def assign_user_issue(db: Session, request: IssueUserAssign) -> IssueUser:
    # Iterate through the list of admin_user_ids in the request
    for admin_user_id in request.admin_user_ids:
        id = generate_id()

        # Create a new ProjectUserModel instance for each admin_user_id
        issue_user = IssueUserModel(
            id=id, issue_id=request.issue_id, admin_user_id=admin_user_id
        )

        db.add(issue_user)
        db.commit()
        db.refresh(issue_user)

    # Retrieve the admin_users based on their ids and create a list
    admin_users = [
        get_admin_user(db, admin_user_id) for admin_user_id in request.admin_user_ids
    ]

    # Set the admin_users list to the project_user instance
    issue_user.admin_users = admin_users
    return issue_user
