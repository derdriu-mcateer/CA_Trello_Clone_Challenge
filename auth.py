from flask import abort
from models.user import User
from setup import db
from flask_jwt_extended import get_jwt_identity

def admin_required():
    user_email = get_jwt_identity()
    stmt = db.select(User).where(User.email == user_email)
    user = db.session.scalar(stmt)
    if not (user and user.admin):
        abort(401)
