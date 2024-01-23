import enum
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.database import Base


class ProjectStatusEnum(enum.Enum):
    """
    PLANNING
    INPROGRESS
    COMPLETED
    ONHOLD
    CANCELLED

    """

    PLANNING = "PLANNING"
    INPROGRESS = "INPROGRESS"
    COMPLETED = "COMPLETED"
    ONHOLD = "ONHOLD"
    CANCELLED = "CANCELLED"


class TaskStatusEnum(enum.Enum):
    """
    PENDING
    INPROGRESS
    COMPLETED

    """

    PENDING = "PENDING"
    INPROGRESS = "INPROGRESS"
    COMPLETED = "COMPLETED"


class IssueStatusEnum(enum.Enum):
    """
    OPEN
    CLOSED

    """

    OPEN = "OPEN"
    CLOSED = "CLOSED"


class IssuePriorityEnum(enum.Enum):
    """
    LOW
    MEDIUM
    HIGH

    """

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class AdminUserModel(Base):
    __tablename__ = "admin_users"

    id = Column(String(36), primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, index=True)
    password = Column(String(255), nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)

    admin_user_role = relationship("AdminUserRoleModel", backref="admin_user")


class AdminUserRoleModel(Base):
    __tablename__ = "admin_user_roles"

    id = Column(String(36), primary_key=True)
    admin_user_id = Column(String(36), ForeignKey("admin_users.id"), nullable=False)
    role_id = Column(String(36), ForeignKey("roles.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)


class RoleModel(Base):
    __tablename__ = "roles"

    id = Column(String(36), primary_key=True)
    slug = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    editable = Column(Boolean, nullable=False, default=True)
    is_deleted = Column(Boolean, nullable=False, default=False, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)

    user_role = relationship("AdminUserRoleModel", backref="role")
    role_operation = relationship("RoleOperationModel", backref="role")


class RoleOperationModel(Base):
    __tablename__ = "role_operations"

    id = Column(String(36), primary_key=True)
    role_id = Column(String(36), ForeignKey("roles.id"), nullable=False)
    operation_id = Column(String(36), ForeignKey("operations.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)


class OperationModel(Base):
    __tablename__ = "operations"

    id = Column(String(36), primary_key=True)
    slug = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    order_index = Column(Integer, nullable=False, index=True)
    parent_id = Column(String(36), nullable=False, default="0")
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)

    role_operation = relationship("RoleOperationModel", backref="operation")


class AdminUserOtpModel(Base):
    __tablename__ = "admin_user_otps"

    id = Column(String(36), primary_key=True)
    otp = Column(String(6), nullable=False)
    is_redeemed = Column(Boolean, nullable=False, default=False, index=True)
    admin_user_id = Column(String(36), ForeignKey("admin_users.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)

    admin_user = relationship("AdminUserModel", backref="otps")


class ProjectModel(Base):
    __tablename__ = "projects"

    id = Column(String(36), primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(
        Enum(ProjectStatusEnum), nullable=False, default=ProjectStatusEnum.PLANNING
    )
    manager_id = Column(String(36), ForeignKey("admin_users.id"), nullable=True)
    is_deleted = Column(Boolean, nullable=False, default=False, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)

    manager = relationship("AdminUserModel", backref="project")


class ModuleTypeModel(Base):
    __tablename__ = "module_types"

    id = Column(String(36), primary_key=True)
    name = Column(String(50), nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)


class ModuleModel(Base):
    __tablename__ = "modules"

    id = Column(String(36), primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False)
    module_type_id = Column(String(36), ForeignKey("module_types.id"), nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)

    project = relationship("ProjectModel", backref="module")
    module_type = relationship("ModuleTypeModel", backref="module")


class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(String(36), primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)
    status = Column(
        Enum(TaskStatusEnum), nullable=False, default=TaskStatusEnum.PENDING
    )
    module_id = Column(String(36), ForeignKey("modules.id"), nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)

    module = relationship("ModuleModel", backref="task")


class IssueModel(Base):
    __tablename__ = "issues"

    id = Column(String(36), primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)
    image = Column(String(255), nullable=False)
    status = Column(Enum(IssueStatusEnum), nullable=False, default=IssueStatusEnum.OPEN)
    priority = Column(
        Enum(IssuePriorityEnum), nullable=False, default=IssuePriorityEnum.LOW
    )
    task_id = Column(String(36), ForeignKey("tasks.id"), nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)

    task = relationship("TaskModel", backref="issue")


class ProjectUserModel(Base):
    __tablename__ = "project_users"

    id = Column(String(36), primary_key=True)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False)
    admin_user_id = Column(String(36), ForeignKey("admin_users.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)

    project = relationship("ProjectModel", backref="project_user")
    admin_user = relationship("AdminUserModel", backref="project_user")


class IssueUserModel(Base):
    __tablename__ = "issue_users"

    id = Column(String(36), primary_key=True)
    issue_id = Column(String(36), ForeignKey("issues.id"), nullable=False)
    admin_user_id = Column(String(36), ForeignKey("admin_users.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)

    issue = relationship("IssueModel", backref="issue_user")
    admin_user = relationship("AdminUserModel", backref="issue_user")
