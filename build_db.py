import sqlalchemy as db
import Login.persistence.model as mod
from sqlalchemy.orm import relationship, sessionmaker

engine = db.create_engine('sqlite:///Login/db/login.sqlite', echo=True, future=True)
mod.Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()