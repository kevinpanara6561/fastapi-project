from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import AdminUserRoleModel, OperationModel, RoleModel, RoleOperationModel
from app.routers.admin.crud.admin_users.admin_users import is_super_admin


def get_operation(db: Session, operation_id: str):
    db_operation = (
        db.query(OperationModel).filter(OperationModel.id == operation_id).first()
    )
    return db_operation


def get_user_operation(db: Session, admin_user_id: str):
    super_admin = is_super_admin(db, admin_user_id=admin_user_id)
    headings = (
        db.query(OperationModel)
        .filter(OperationModel.parent_id == "0")
        .order_by(OperationModel.order_index)
        .all()
    )
    all_operations = []
    allowed_menu = []
    for heading in headings:
        if super_admin:
            rows = (
                db.query(OperationModel)
                .filter(OperationModel.parent_id == heading.id)
                .order_by(OperationModel.order_index)
                .all()
            )
        else:
            rows = (
                db.query(OperationModel)
                .filter(OperationModel.parent_id == heading.id)
                .order_by(OperationModel.order_index)
                .join(RoleOperationModel)
                .join(RoleModel)
                .join(AdminUserRoleModel)
                .filter(AdminUserRoleModel.admin_user_id == admin_user_id)
                .all()
            )
        operations = []
        for row in rows:
            operations.append(row.slug)
        all_operations.extend(operations)
        if len(operations) == 0:
            continue
        allowed_menu.append(heading.slug)
    data = {"operations": all_operations, "menu": allowed_menu}
    return data


def get_all_operations(db: Session):
    headings = (
        db.query(OperationModel)
        .filter(OperationModel.parent_id == "0")
        .order_by(OperationModel.order_index)
        .all()
    )
    for heading in headings:
        operations = (
            db.query(OperationModel)
            .filter(OperationModel.parent_id == heading.id)
            .order_by(OperationModel.order_index)
            .all()
        )
        heading.operations = operations
    return headings


def verify_admin_user_operation(db: Session, admin_user_id: str, operation: str):
    super_admin = is_super_admin(db, admin_user_id=admin_user_id)
    if not super_admin:
        db_operations = (
            db.query(AdminUserRoleModel)
            .filter(AdminUserRoleModel.admin_user_id == admin_user_id)
            .join(RoleModel)
            .join(RoleOperationModel)
            .join(OperationModel)
            .filter(OperationModel.slug == operation)
            .first()
        )
        if db_operations is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You don't have permission.",
            )


def get_modules(db: Session):
    db_modules = db.query(OperationModel).filter(OperationModel.parent_id == 0).all()
    return db_modules
