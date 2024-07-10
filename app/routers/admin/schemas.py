from __future__ import annotations

from datetime import date
from typing import Dict, List, Optional

from email_validator import EmailNotValidError, validate_email
from fastapi import HTTPException, status
from pydantic import BaseModel, ConfigDict, Field, validator

from app.models.issues.models import (
    IssuePriorityEnum,
    IssueStatusEnum,
)
from app.models.projects.models import ProjectStatusEnum
from app.models.tasks.models import TaskStatusEnum
from app.models.issues.models import IssuePriorityEnum
from app.libs.utils import now


class AdminUserChangePassword(BaseModel):
    old_password: str = Field(min_length=6, max_length=50)
    new_password: str = Field(min_length=6, max_length=50)


class AdminUserResetPassword(BaseModel):
    new_password: str = Field(min_length=6, max_length=50)


class Role(BaseModel):
    id: str
    name: str
    editable: bool

    class Config:
        orm_mode = True


class RoleList(BaseModel):
    count: int
    list: List[Role]


class OperationMaster(BaseModel):
    id: str
    name: str

    class Config:
        orm_mode = True


class RoleDetails(BaseModel):
    id: str
    name: str
    operations: List[OperationMaster] = Field(description="Operation Id")

    class Config:
        orm_mode = True


class RoleAdd(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    operations: List[str] = Field(description="Operation Id")

    # @field_validator("operations")
    # @classmethod
    # def valid_operations(cls, operations):
    #     if len(operations) > 0:
    #         return operations
    #     else:
    #         raise HTTPException(
    #             status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    #             detail="Ensure operations has at least 1 operation id.",
    #         )


class Operation(BaseModel):
    id: str
    name: str
    # model_config = ConfigDict(from_attributes=True)

    class Config:
        orm_mode = True


class OperationList(BaseModel):
    count: int
    list: List[Operation]
    model_config = ConfigDict(from_attributes=True)


class RoleOperation(BaseModel):
    id: str
    name: str
    operations: List[Operation]
    # model_config = ConfigDict(from_attributes=True)

    class Config:
        orm_mode = True


class AdminUser(BaseModel):
    id: str
    name: str
    email: str
    role: Optional[Role] = None

    class Config:
        orm_mode = True


class AdminUserAll(BaseModel):
    id: str
    name: str
    email: str
    role: Optional[Role] = None

    class Config:
        orm_mode = True


class AdminUserList(BaseModel):
    count: int
    list: List[AdminUserAll]


class AdminUserSmall(BaseModel):
    id: str
    name: str

    class Config:
        orm_mode = True


class Login(BaseModel):
    email: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=6, max_length=50)

    # @field_validator("email")
    # @classmethod
    # def valid_email(cls, email):
    #     try:
    #         valid = validate_email(email)
    #         return valid.email
    #     except EmailNotValidError as e:
    #         raise HTTPException(
    #             status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
    #         )


class LoginResponse(BaseModel):
    id: str
    name: str
    email: str
    role: Optional[Role] = None
    token: str

    class Config:
        orm_mode = True


class ForgotPassword(BaseModel):
    email: str = Field(min_length=3, max_length=100)
    # captcha_token: str = Field(max_length=10000)

    # @field_validator("email")
    # @classmethod
    # def valid_email(cls, email):
    #     try:
    #         valid = validate_email(email)
    #         return valid.email
    #     except EmailNotValidError as e:
    #         raise HTTPException(
    #             status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
    #         )


class VerifyOtp(BaseModel):
    email: str = Field(min_length=3, max_length=100)
    otp: str = Field(min_length=6, max_length=6)


class ConfirmForgotPassword(BaseModel):
    email: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=6, max_length=50)
    confirm_password: str = Field(min_length=6, max_length=50)


class VerifyOtpResponse(BaseModel):
    email: str
    otp: str

    # @field_validator("email")
    # @classmethod
    # def valid_email(cls, email):
    #     try:
    #         valid = validate_email(email)
    #         return valid.email
    #     except EmailNotValidError as e:
    #         raise HTTPException(
    #             status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
    #         )


class ChangePassword(BaseModel):
    password: str = Field(min_length=6, max_length=50)
    new_password: str = Field(min_length=6, max_length=50)


class AdminUserUpdate(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    email: str = Field(min_length=5, max_length=100)
    role_id: str = Field(min_length=36, max_length=36)

    # @field_validator("email")
    # @classmethod
    # def valid_email(cls, email):
    #     try:
    #         valid = validate_email(email)
    #         return valid.email
    #     except EmailNotValidError as e:
    #         raise HTTPException(
    #             status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
    #         )


class AdminUserAdd(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    email: str = Field(min_length=5, max_length=100)
    password: str = Field(min_length=6, max_length=50)
    role_id: str = Field(min_length=36, max_length=36)

    # @field_validator("email")
    # @classmethod
    # def valid_email(cls, email):
    #     try:
    #         valid = validate_email(email)
    #         return valid.email
    #     except EmailNotValidError as e:
    #         raise HTTPException(
    #             status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
    #         )


class AdminUserProfileUpdate(BaseModel):
    name: str = Field(min_length=3, max_length=100)


class MyProfile(BaseModel):
    id: str
    name: str
    email: str

    class Config:
        orm_mode = True


class ModuleType(BaseModel):
    id: str
    name: str

    class Config:
        orm_mode = True


class ModuleTypeList(BaseModel):
    count: int
    list: List[ModuleType]

    class Config:
        orm_mode = True


class ModuleTypeAdd(BaseModel):
    name: str = Field(min_length=3, max_length=50)


class Master(BaseModel):
    id: str
    name: str

    class Config:
        orm_mode = True


class Project(BaseModel):
    id: str
    name: str
    description: Optional[str]
    start_date: date
    end_date: date
    status: ProjectStatusEnum
    manager: Master

    class Config:
        orm_mode = True


class ProjectList(BaseModel):
    count: int
    list: List[Project]

    class Config:
        orm_mode = True


class ProjectAdd(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    description: Optional[str] = Field(min_length=3, max_length=50)
    start_date: date
    end_date: date
    manager_id: str = Field(min_length=36, max_length=36)


class ProjectStatusChange(BaseModel):
    project_id: str = Field(min_length=36, max_length=36)
    status: ProjectStatusEnum


class Module(BaseModel):
    id: str
    name: str
    description: str
    project: Master
    module_type: Master

    class Config:
        orm_mode = True


class ModuleList(BaseModel):
    count: int
    list: List[Module]

    class Config:
        orm_mode = True


class ModuleAdd(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    description: str = Field(min_length=3, max_length=50)
    project_id: str = Field(min_length=36, max_length=36)
    module_type_id: str = Field(min_length=36, max_length=36)


class Task(BaseModel):
    id: str
    name: str
    description: Optional[str]
    status: TaskStatusEnum
    module: Master

    class Config:
        orm_mode = True


class TaskList(BaseModel):
    count: int
    list: List[Task]

    class Config:
        orm_mode = True


class TaskAdd(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    description: Optional[str] = Field(min_length=3, max_length=50)
    module_id: str = Field(min_length=36, max_length=36)


class TaskStatusChange(BaseModel):
    task_id: str = Field(min_length=36, max_length=36)
    status: TaskStatusEnum


class Issue(BaseModel):
    id: str
    name: str
    description: Optional[str]
    status: IssueStatusEnum
    priority: IssuePriorityEnum
    task: Master

    class Config:
        orm_mode = True


class IssuesList(BaseModel):
    count: int
    list: List[Issue]

    class Config:
        orm_mode = True


class IssueAdd(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    description: Optional[str] = Field(min_length=3, max_length=50)
    task_id: str = Field(min_length=36, max_length=36)


class ProjectUserAssign(BaseModel):
    project_id: str = Field(min_length=36, max_length=36)
    admin_user_ids: List[str] = Field(min_items=1, min_length=36, max_length=36)

    @validator("admin_user_ids")
    def validate_admin_user_ids(cls, admin_user_ids):
        # Check for duplicate IDs in admin_user_ids
        if len(admin_user_ids) != len(set(admin_user_ids)):
            raise ValueError("Duplicate admin_user_ids are not allowed.")
        return admin_user_ids


class ProjectUser(BaseModel):
    project: Master
    admin_users: List[Master]

    class Config:
        orm_mode = True


class IssueUserAssign(BaseModel):
    issue_id: str = Field(min_length=36, max_length=36)
    admin_user_ids: List[str] = Field(min_items=1, min_length=36, max_length=36)

    @validator("admin_user_ids")
    def validate_admin_user_ids(cls, admin_user_ids):
        # Check for duplicate IDs in admin_user_ids
        if len(admin_user_ids) != len(set(admin_user_ids)):
            raise ValueError("Duplicate admin_user_ids are not allowed.")
        return admin_user_ids


class IssueUser(BaseModel):
    issue: Master
    admin_users: List[Master]

    class Config:
        orm_mode = True
