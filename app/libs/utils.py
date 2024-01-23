import hashlib
import os
import pathlib
import random
import traceback
import urllib.request
from datetime import datetime
from mimetypes import guess_extension
from typing import Optional
from uuid import uuid4

import boto3
# from datauri import DataURI
from datauri.exceptions import InvalidDataURI
from fastapi import HTTPException, status
from sqlalchemy import desc, inspect, or_
from sqlalchemy.orm import Session

from app.config import BUCKET_NAME


def now():
    return datetime.now()


def generate_id():
    return str(uuid4())


def generate_key():
    return uuid4().hex


def generate_otp():
    otp = ""
    while len(otp) < 6:
        otp += str(random.randint(0, 9))
    return otp


def date_time_diff_min(start: datetime, end: datetime):
    duration = end - start
    duration_in_seconds = duration.total_seconds()
    minutes = divmod(duration_in_seconds, 60)[0]
    return minutes


def remove_file(path):
    os.remove(path)


def create_hash(key: str) -> str:
    key = key.encode()
    key = hashlib.sha256(key).digest()
    key = key.decode("unicode_escape")
    return key


# def my_logo(data_uri=""):
#     try:
#         uri = DataURI(data_uri)
#     except InvalidDataURI:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid DataURI."
#         )
#     mime_type = uri.mimetype
#     file_extension = guess_extension(mime_type)
#     # Use the generated UUID for creating the file path
#     generated_uuid = generate_id()
#     file_path = os.path.join("app", "uploads", generated_uuid + file_extension)

#     # Use the 'file_path' to open and write the image data
#     with open(file_path, "wb") as fd:
#         fd.write(uri.data)

#     return file_extension, generated_uuid, file_path


# def upload_file_using_resource(file_path, generated_uuid, file_extension):
#     s3 = boto3.resource("s3")
#     object_name = f"assets/{generated_uuid}{file_extension}"
#     try:
#         bucket = s3.Bucket(BUCKET_NAME)
#         bucket.upload_file(file_path, object_name)
#     except Exception as e:
#         print(e)
#         print(traceback.format_exc())
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Image upload failed.",
#         )
#     return object_name


def list_data(
    db: Session,
    model,
    start: int,
    limit: int,
    sort_by: Optional[str] = None,
    order: Optional[str] = None,
    search: Optional[str] = None,
):
    # Create the base query
    query = db.query(model).filter(model.is_deleted == False)

    # Apply search filters if a search term is provided
    if search:
        text = f"%{search}%"
        columns = inspect(model).columns.keys()
        # Use dynamic filtering for all string columns
        text_filters = [getattr(model, col).ilike(text) for col in columns]
        query = query.filter(or_(*text_filters))

    # Apply sorting if a sort_by parameter is provided
    if sort_by:
        column = getattr(model, sort_by, None)
        if column:
            if order == "desc":
                query = query.order_by(desc(column))
            else:
                query = query.order_by(column)

    # If no sort_by parameter is provided, default to sorting by created_at in descending order
    else:
        query = query.order_by(desc(model.created_at))

    # Execute the query with pagination
    results = query.offset(start).limit(limit).all()
    count = query.count()
    data = {"count": count, "list": results}
    return data
