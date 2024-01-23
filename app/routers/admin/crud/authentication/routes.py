from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.routers.admin.crud.admin_users import admin_users
from app.routers.admin.schemas import (
    ConfirmForgotPassword,
    ForgotPassword,
    Login,
    LoginResponse,
    VerifyOtp,
)

router = APIRouter(tags=["Authentication"])


@router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginResponse)
def sign_in(admin_user: Login, db: Session = Depends(get_db)):
    data = admin_users.sign_in(db, admin_user)
    return data


@router.post("/forgot-password")
def send_forgot_password_email(
    admin_user: ForgotPassword, db: Session = Depends(get_db)
):
    data = admin_users.send_forgot_password_email(db=db, admin_user=admin_user)
    return data


@router.post("/verify-otp", status_code=status.HTTP_200_OK)
def verify_otp(admin_user: VerifyOtp, db: Session = Depends(get_db)):
    data = admin_users.verify_otp(db=db, admin_user=admin_user)
    return data


@router.put("/forgot-password")
def confirm_forgot_password(
    admin_user: ConfirmForgotPassword, db: Session = Depends(get_db)
):
    data = admin_users.confirm_forgot_password(db=db, admin_user=admin_user)
    return data
