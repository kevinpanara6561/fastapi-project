from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
from app.models.models import ProjectModel

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