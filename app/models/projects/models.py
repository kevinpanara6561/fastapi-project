import enum
from sqlalchemy import Column, String, Boolean, DateTime, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
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

class ProjectModel(Base):
    __tablename__ = "projects"

    id = Column(String(36), primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(Enum(ProjectStatusEnum), nullable=False, default=ProjectStatusEnum.PLANNING)
    manager_id = Column(String(36), ForeignKey("admin_users.id"), nullable=True)
    is_deleted = Column(Boolean, nullable=False, default=False, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)

    manager = relationship("AdminUserModel", backref="project")

class ProjectUserModel(Base):
    __tablename__ = "project_users"

    id = Column(String(36), primary_key=True)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False)
    admin_user_id = Column(String(36), ForeignKey("admin_users.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)

    project = relationship("ProjectModel", backref="project_user")
    admin_user = relationship("AdminUserModel", backref="project_user")
