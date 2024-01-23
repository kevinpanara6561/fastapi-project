# seed.py
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER
from app.models import (
    AdminUserModel,
    AdminUserOtpModel,
    AdminUserRoleModel,
    IssueModel,
    IssueUserModel,
    ModuleModel,
    ModuleTypeModel,
    OperationModel,
    ProjectModel,
    ProjectUserModel,
    RoleModel,
    RoleOperationModel,
    TaskModel,
)

fake = Faker()

DB_POOL_SIZE = 100  # Adjust as needed
WEB_CONCURRENCY = 2  # Adjust as needed
POOL_SIZE = max(DB_POOL_SIZE // WEB_CONCURRENCY, 5)

SQLALCHEMY_DATABASE_URL = (
    "mysql+pymysql://" + DB_USER + ":" + DB_PASSWORD + "@" + DB_HOST + "/" + DB_NAME
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, pool_size=POOL_SIZE, max_overflow=0, pool_recycle=3600
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_fake_admin_user():
    return AdminUserModel(
        name=fake.name(),
        email=fake.email(),
        password=fake.password(),
    )


def create_fake_role():
    return RoleModel(
        slug=fake.word(),
        name=fake.word(),
        editable=fake.boolean(),
    )


# Add similar functions for other models


def seed_data():
    # Seed Admin Users
    admin_users = [create_fake_admin_user() for _ in range(10)]
    SessionLocal.bulk_save_objects(admin_users)

    # Seed Roles
    roles = [create_fake_role() for _ in range(5)]
    SessionLocal.bulk_save_objects(roles)

    # Add seeding logic for other models

    SessionLocal.commit()

    print("Seeding completed.")


# Run seeding when this script is executed
seed_data()
