from datetime import date
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Date, ForeignKey, Text, LargeBinary
from datetime import datetime

class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class = Base)


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[str] = mapped_column(Text, default='user')
    email: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(Text, nullable=False)
    first_name: Mapped[str] = mapped_column(Text)
    last_name: Mapped[str] = mapped_column(Text)
    gender: Mapped[str] = mapped_column(Text)
    birthdate: Mapped[date] = mapped_column(Date)
    in_game_name: Mapped[str] = mapped_column(Text)
    tagline: Mapped[str] = mapped_column(Text)
    bio: Mapped[str] = mapped_column(Text)
    # picture: Mapped[bytes] = mapped_column(LargeBinary, nullable=True, default=None)
    city: Mapped[str] = mapped_column(Text)
    state: Mapped[str] = mapped_column(Text)
    country: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.now)
    
    matches: Mapped[list['Matches']] = relationship('Matches', foreign_keys='[Matches.user1_id]', back_populates='user1')
    matches_: Mapped[list['Matches']] = relationship('Matches', foreign_keys='[Matches.user2_id]', back_populates='user2')
    messages: Mapped[list['Messages']] = relationship('Messages', foreign_keys='[Messages.receiver_id]', back_populates='receiver')
    messages_: Mapped[list['Messages']] = relationship('Messages', foreign_keys='[Messages.sender_id]', back_populates='sender')




class Matches(Base):
    __tablename__ = 'matches'

    id: Mapped[int] = mapped_column(primary_key=True)
    user1_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    user2_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    status: Mapped[str] = mapped_column(Text, default='accepted')
    created_at: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.now)
    
    user1: Mapped['Users'] = relationship('Users', foreign_keys=[user1_id], back_populates='matches')
    user2: Mapped['Users'] = relationship('Users', foreign_keys=[user2_id], back_populates='matches_')



class Messages(Base):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(primary_key=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    receiver_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.now)
    read: Mapped[bool] = mapped_column(db.Boolean, default=False)
    
    receiver: Mapped['Users'] = relationship('Users', foreign_keys=[receiver_id], back_populates='messages')
    sender: Mapped['Users'] = relationship('Users', foreign_keys=[sender_id], back_populates='messages_')
