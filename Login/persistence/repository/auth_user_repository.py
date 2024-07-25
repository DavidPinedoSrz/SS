import sqlalchemy as db
from Login.persistence.model import Auth_User
from sqlalchemy.orm import Session


class AuthUserRepositroy():

    def __init__(self):
        self.engine = db.create_engine('sqlite:///Login/db/login.sqlite',
                                       echo=True, future=True)

    def getUserById(self, user_id: int):
        user: Auth_User = None
        with Session(self.engine) as session:
            user = session.query(Auth_User).filter_by(
                id=user_id).first()
        return user

    def insertUser(self, user: Auth_User):
        with Session(self.engine) as session:
            session.add(user)
            session.commit()