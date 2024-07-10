import enum
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
from app.models.modules.models import ModuleModel

class TaskStatusEnum(enum.Enum):
    """
    PENDING
    INPROGRESS
    COMPLETED

    """

    PENDING = "PENDING"
    INPROGRESS = "INPROGRESS"
    COMPLETED = "COMPLETED"
    
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