from sqlalchemy import Column
from sqlalchemy import String, Integer, Enum, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

# Tabla de asociación entre Event y Participant
event_participant_table = Table('event_participant', Base.metadata,
    Column('event_id', Integer, ForeignKey('events.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('auth_user.id'), primary_key=True),
    Column('status', String)  # Status puede ser "accepted" o "rejected"
)

class Auth_User(Base):
    __tablename__ = "auth_user"
    id = Column(Integer, primary_key=True)
    username = Column(String(150))
    lastname = Column(String(150))
    password = Column(String(128))
    rol = Column(Enum('Administrador', 'Organizador', 'Participante'))

    # Relaciones
    events = relationship('Event', secondary=event_participant_table, back_populates='participants')
    notifications = relationship('Notification', back_populates='user')
    organized_events = relationship('Event', back_populates='organizer')

    def __repr__(self):
        return f'auth_user({self.username}, {self.password})'

    def __str__(self):
        return self.username
    
class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    date = Column(DateTime, nullable=False)
    location = Column(String)
    is_online = Column(Boolean, default=False)
    organizer_id = Column(Integer, ForeignKey('auth_user.id'), nullable=False)
    
    # Relaciones
    organizer = relationship('Auth_User', back_populates='organized_events')
    participants = relationship('Auth_User', secondary=event_participant_table, back_populates='events')
    notifications = relationship('Notification', back_populates='event')
    resources = relationship('Resource', back_populates='event')

class Resource(Base):
    __tablename__ = 'resources'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    status = Column(String, nullable=False)  # Ej. "available", "unavailable"
    event_id = Column(Integer, ForeignKey('events.id'))

    # Relaciones
    event = relationship('Event', back_populates='resources')

class Notification(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True)
    message = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('auth_user.id'))
    event_id = Column(Integer, ForeignKey('events.id'))

    # Relaciones
    user = relationship('Auth_User', back_populates='notifications')
    event = relationship('Event', back_populates='notifications')