import json
import traceback
from typing import Optional

import bcrypt
from fastapi import HTTPException, status
from jwcrypto import jwk, jwt
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.config import JWT_KEY
from app.libs.emails import send_email
from app.libs.recaptcha import verify_captcha
from app.libs.utils import date_time_diff_min, generate_id, generate_otp, now
from app.models import AdminUserModel, AdminUserOtpModel, AdminUserRoleModel, RoleModel
from app.routers.admin.crud.common.email_templates import forgot_password
from app.routers.admin.schemas import (
    AdminUserAdd,
    AdminUserChangePassword,
    AdminUserProfileUpdate,
    AdminUserResetPassword,
    AdminUserUpdate,
    ConfirmForgotPassword,
    ForgotPassword,
    Login,
    LoginResponse,
    VerifyOtp,
)


def get_token(admin_user_id, email):
    claims = {"id": admin_user_id, "email": email, "time": str(now())}

    # Create a signed token with the generated key
    key = jwk.JWK(**JWT_KEY)
    token = jwt.JWT(header={"alg": "HS256"}, claims=claims)
    token.make_signed_token(key)

    # Further encrypt the token with the same key
    encrypted_token = jwt.JWT(
        header={"alg": "A256KW", "enc": "A256CBC-HS512"}, claims=token.serialize()
    )
    encrypted_token.make_encrypted_token(key)
    return encrypted_token.serialize()


def verify_token(db: Session, token: str):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token"
        )
    else:
        try:
            key = jwk.JWK(**JWT_KEY)
            ET = jwt.JWT(key=key, jwt=token)
            ST = jwt.JWT(key=key, jwt=ET.claims)
            claims = ST.claims
            claims = json.loads(claims)
            db_admin_user = get_admin_user_by_id(db, id=claims["id"])
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if db_admin_user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="ADMIN_USER_NOT_FOUND"
            )
        elif db_admin_user.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="ADMIN_USER_NOT_FOUND"
            )
        return db_admin_user


def create_password(password: str) -> str:
    password = password.encode("utf-8")
    password = bcrypt.hashpw(password, bcrypt.gensalt(4))
    password = password.decode("utf-8")
    return password


def get_admin_user_by_id(db: Session, id: str):
    return (
        db.query(AdminUserModel)
        .filter(AdminUserModel.id == id, AdminUserModel.is_deleted == False)
        .first()
    )


def get_admin_user_by_email(db: Session, email: str):
    return (
        db.query(AdminUserModel)
        .filter(AdminUserModel.email == email, AdminUserModel.is_deleted == False)
        .first()
    )


def sign_in(db: Session, admin_user: Login) -> LoginResponse:
    db_admin_user = get_admin_user_by_email(db, email=admin_user.email)

    if db_admin_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    elif db_admin_user.is_deleted:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    hashed = db_admin_user.password.encode("utf-8")
    password = admin_user.password.encode("utf-8")

    if not bcrypt.checkpw(password, hashed):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    db_admin_user.token = get_token(db_admin_user.id, db_admin_user.email)
    db_admin_user.role = get_admin_user_role(db, admin_user_id=db_admin_user.id)
    return db_admin_user


def change_password(db: Session, admin_user: AdminUserChangePassword, token: str):
    db_admin_user = verify_token(db, token=token)
    try:
        hashed = bytes(db_admin_user.password, "utf-8")
        password = bytes(admin_user.old_password, "utf-8")
        result = bcrypt.checkpw(password, hashed)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect old password"
        )

    password = create_password(admin_user.new_password)
    db_admin_user.password = password
    db_admin_user.updated_at = now()
    db.commit()


def reset_password(db: Session, admin_user: AdminUserResetPassword, admin_user_id: str):
    db_admin_user = get_admin_user_by_id(db, id=admin_user_id)
    if db_admin_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ADMIN_USER_NOT_FOUND"
        )
    else:
        hashed = create_password(admin_user.new_password)
        db_admin_user.password = hashed
        db_admin_user.updated_at = now()
        db.commit()


def get_admin_user_role(db: Session, admin_user_id: str) -> RoleModel:
    db_role = (
        db.query(RoleModel)
        .join(AdminUserRoleModel)
        .filter(AdminUserRoleModel.admin_user_id == admin_user_id)
        .first()
    )
    return db_role


def get_profile(db: Session, token: str):
    db_admin_user = verify_token(db, token=token)
    return db_admin_user


def is_super_admin(db: Session, admin_user_id: str):
    db_role = get_admin_user_role(db, admin_user_id=admin_user_id)
    status = True if db_role.slug == "Super Admin" else False
    return status


def send_forgot_password_email(db: Session, admin_user: ForgotPassword):
    # verify_captcha(captcha_token=admin_user.captcha_token)
    db_admin_user = get_admin_user_by_email(db=db, email=admin_user.email)
    if not db_admin_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    otp = generate_otp()
    db_otp = AdminUserOtpModel(
        id=generate_id(),
        otp=otp,
        admin_user_id=db_admin_user.id,
    )
    db.add(db_otp)
    email_body = forgot_password(name=db_admin_user.name, otp=otp)
    if not send_email(
        recipients=[db_admin_user.email], subject="Forgot Password", body=email_body
    ):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error while sending email.",
        )
    db.commit()

    return "Email sent"


def verify_otp(db: Session, admin_user: VerifyOtp):
    db_admin_user = get_admin_user_by_email(db=db, email=admin_user.email)
    if not db_admin_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email not registered",
        )

    date_time = now()
    db_otp = (
        db.query(AdminUserOtpModel)
        .filter(AdminUserOtpModel.admin_user_id == db_admin_user.id)
        .order_by(AdminUserOtpModel.created_at.desc())
        .first()
    )
    if db_otp.is_redeemed:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid OTP."
        )
    elif date_time_diff_min(start=db_otp.created_at, end=date_time) >= 10:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="OTP expired."
        )
    elif db_otp.otp != admin_user.otp:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid OTP."
        )

    db_admin_user.updated_at = now()
    db_otp.is_redeemed = True
    db_otp.updated_at = now()
    db.commit()

    return "Otp verified"


def confirm_forgot_password(db: Session, admin_user: ConfirmForgotPassword):
    db_admin_user = get_admin_user_by_email(db=db, email=admin_user.email)
    if not db_admin_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email not registered",
        )

    if admin_user.password != admin_user.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password and confirm password should not be same",
        )
    db_admin_user.password = create_password(admin_user.password)
    db.commit()

    return "Password changed"


def get_admin_user_for_list(db: Session, id: str):
    db_admin_user = db.query(AdminUserModel).filter(AdminUserModel.id == id).first()
    if db_admin_user is None:
        return {}
    name = db_admin_user.first_name + " " + db_admin_user.last_name
    data = {"id": db_admin_user.id, "name": name}
    return data


def update_admin_user_role(db: Session, admin_user_id: str, role_id: str):
    db.query(AdminUserRoleModel).filter(
        AdminUserRoleModel.admin_user_id == admin_user_id
    ).delete()
    db_admin_user_role = AdminUserRoleModel(
        id=generate_id(), admin_user_id=admin_user_id, role_id=role_id
    )
    db.add(db_admin_user_role)
    db.commit()


def throw_error_if_super_admin_role(db: Session, role_id: str):
    db_role = db.query(RoleModel).filter(RoleModel.id == role_id).first()
    if db_role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role not found."
        )
    elif db_role.slug == "Super Admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


def add_admin_user(db: Session, admin_user: AdminUserAdd):
    db_admin_user = get_admin_user_by_email(db, email=admin_user.email)
    if db_admin_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exist."
        )

    admin_user.password = create_password(admin_user.password)
    admin_user = admin_user.dict()
    role_id = admin_user["role_id"]
    throw_error_if_super_admin_role(db=db, role_id=role_id)

    del admin_user["role_id"]
    admin_user_id = generate_id()
    db_admin_user = AdminUserModel(id=admin_user_id, **admin_user)
    db.add(db_admin_user)
    db.commit()
    db.refresh(db_admin_user)
    update_admin_user_role(db, admin_user_id=admin_user_id, role_id=role_id)
    return db_admin_user.id


def get_admin_users(
    db: Session,
    start: int,
    limit: int,
    sort_by: Optional[str] = None,
    order: Optional[str] = None,
    search: Optional[str] = None,
):
    query = db.query(AdminUserModel).filter(AdminUserModel.is_deleted == False)

    if search:
        text = f"""%{search}%"""
        query = query.filter(
            or_(
                AdminUserModel.name.like(text),
                AdminUserModel.email.like(text),
            )
        )

    if sort_by == "name":
        if order == "desc":
            query = query.order_by(AdminUserModel.name.desc())
        else:
            query = query.order_by(AdminUserModel.name)
    elif sort_by == "email":
        if order == "desc":
            query = query.order_by(AdminUserModel.email.desc())
        else:
            query = query.order_by(AdminUserModel.email)
    else:
        query = query.order_by(AdminUserModel.created_at.desc())

    results = query.offset(start).limit(limit).all()
    count = query.count()
    for admin_user in results:
        admin_user_role = get_admin_user_role(db, admin_user.id)
        admin_user.role = admin_user_role
    data = {"count": count, "list": results}
    return data


def delete_admin_user(db: Session, admin_user_id: str):
    db_admin_user = get_admin_user_by_id(db, id=admin_user_id)

    if db_admin_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ADMIN_USER_NOT_FOUND"
        )

    if is_super_admin(db=db, admin_user_id=admin_user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    db_admin_user.is_deleted = True
    db_admin_user.updated_at = now()
    db.commit()


def update_profile(db: Session, admin_user: AdminUserProfileUpdate, token: str):
    db_admin_user = verify_token(db, token=token)
    db_admin_user.name = admin_user.name
    db_admin_user.updated_at = now()
    db.commit()
    return db_admin_user


def get_admin_user(db: Session, admin_user_id: str):
    db_admin_user = get_admin_user_by_id(db, id=admin_user_id)
    if db_admin_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ADMIN_USER_NOT_FOUND"
        )
    db_admin_user.role = db_admin_user.admin_user_role[0].role
    return db_admin_user


def update_admin_user(db: Session, admin_user_id: str, admin_user: AdminUserUpdate):
    db_admin_user = get_admin_user_by_id(db, id=admin_user_id)
    if db_admin_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ADMIN_USER_NOT_FOUND"
        )

    if admin_user.email != db_admin_user.email:
        _db_admin_user = get_admin_user_by_email(db, email=admin_user.email)
        if _db_admin_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Email already exists."
            )

    db_admin_user.name = admin_user.name
    db_admin_user.email = admin_user.email
    db.commit()
    db.refresh(db_admin_user)
    if db_admin_user.admin_user_role[0].role.id != admin_user.role_id:
        throw_error_if_super_admin_role(db=db, role_id=admin_user.role_id)
        update_admin_user_role(
            db, admin_user_id=admin_user_id, role_id=admin_user.role_id
        )
    db_admin_user = get_admin_user(db, admin_user_id=admin_user_id)
    return db_admin_user


def get_all_admin_users(db: Session):
    db_admin_users = (
        db.query(AdminUserModel)
        .filter(AdminUserModel.is_deleted == False)
        .order_by(AdminUserModel.name)
        .all()
    )
    return db_admin_users
