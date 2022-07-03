from sqlalchemy.orm import Session

from schemas import UserIn
import crud

def login(user: UserIn, db: Session) -> bool:
    if crud.query_user(user, db) is None:
        crud.insert_user(user, db)
    
    return True