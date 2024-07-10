import enum
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

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