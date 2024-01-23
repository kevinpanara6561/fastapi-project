from typing import Optional

from fastapi import APIRouter, Depends, Header, Path, Query, Response, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.libs.constants import ISSUE_ID, ORDER_BY, TASK_ID
from app.routers.admin.crud.admin_users import admin_users
from app.routers.admin.crud.issues import issues
from app.routers.admin.crud.operations import operations
from app.routers.admin.schemas import (
    Issue,
    IssueAdd,
    IssuesList,
    IssueUser,
    IssueUserAssign,
)

router = APIRouter(prefix="/issues", tags=["Issues"])


@router.get("", response_model=IssuesList)
def get_issues(
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
    data = issues.get_issues(
        db, start=start, limit=limit, sort_by=sort_by, order=order, search=search
    )
    return data


@router.get("/{issue_id}", response_model=Issue)
def get_issue(
    token: str = Header(None),
    issue_id: str = Path(title=TASK_ID, min_length=36, max_length=36),
    db: Session = Depends(get_db),
):
    db_admin_user = admin_users.verify_token(db, token=token)
    # operations.verify_admin_user_operation(
    #     db, admin_user_id=db_admin_user.id, operation="Edit Admin User"
    # )
    data = issues.get_issue(db, issue_id=issue_id)
    return data


@router.post("", status_code=status.HTTP_201_CREATED, response_model=Issue)
def add_issue(
    request: IssueAdd,
    token: str = Header(None),
    db: Session = Depends(get_db),
):
    db_admin_user = admin_users.verify_token(db, token=token)
    # operations.verify_admin_user_operation(
    #     db, admin_user_id=db_admin_user.id, operation="Add Admin User"
    # )
    data = issues.add_issue(db, request=request)
    return data


@router.put("/{issue_id}", response_model=Issue)
def update_issue(
    request: IssueAdd,
    token: str = Header(None),
    issue_id: str = Path(title=ISSUE_ID, min_length=36, max_length=36),
    db: Session = Depends(get_db),
):
    db_admin_user = admin_users.verify_token(db, token=token)
    # operations.verify_admin_user_operation(
    #     db, admin_user_id=db_admin_user.id, operation="Edit Admin User"
    # )
    data = issues.update_issue(db, issue_id=issue_id, request=request)
    return data


@router.delete("/{issue_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_issue(
    token: str = Header(None),
    issue_id: str = Path(title=ISSUE_ID, min_length=36, max_length=36),
    db: Session = Depends(get_db),
):
    db_admin_user = admin_users.verify_token(db, token=token)
    # operations.verify_admin_user_operation(
    #     db, admin_user_id=db_admin_user.id, operation="Delete Admin User"
    # )
    issues.delete_issue(db, issue_id=issue_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/{issue_id}/close")
def close_issue(
    token: str = Header(None),
    issue_id: str = Path(title=ISSUE_ID, min_length=36, max_length=36),
    db: Session = Depends(get_db),
):
    db_admin_user = admin_users.verify_token(db, token=token)
    # operations.verify_admin_user_operation(
    #     db, admin_user_id=db_admin_user.id, operation="Delete Admin User"
    # )

    issues.close_issue(db, issue_id=issue_id)
    return "Issue is Closed"


@router.post(
    "/assign_issue", status_code=status.HTTP_201_CREATED, response_model=IssueUser
)
def assign_user_issue(
    request: IssueUserAssign,
    token: str = Header(None),
    db: Session = Depends(get_db),
):
    db_admin_user = admin_users.verify_token(db, token=token)
    # operations.verify_admin_user_operation(
    #     db, admin_user_id=db_admin_user.id, operation="Add Admin User"
    # )
    data = issues.assign_user_issue(db, request=request)
    return data
