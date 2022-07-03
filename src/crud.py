from datetime import datetime

from sqlalchemy.orm import Session

from models import User
from schemas import UserIn


def query_user(user: UserIn, db: Session) -> User:
    return db.query(User).get((user.id, user.type))

def insert_user(user: UserIn, db: Session) -> None:
    db_user = User(
        id=user.id,
        nick_name=user.nick_name,
        avatar_url=user.avatar_url,
        type=user.type,
        created_time=datetime.utcnow()
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
