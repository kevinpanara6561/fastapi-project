from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

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

class AdminUserOtpModel(Base):
    __tablename__ = "admin_user_otps"

    id = Column(String(36), primary_key=True)
    otp = Column(String(6), nullable=False)
    is_redeemed = Column(Boolean, nullable=False, default=False, index=True)
    admin_user_id = Column(String(36), ForeignKey("admin_users.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)

    admin_user = relationship("AdminUserModel", backref="otps")

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