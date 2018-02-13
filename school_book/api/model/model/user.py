from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship
from school_book.api.model.model.config import Base
from school_book.api.views.helper.helper import new_salt
from school_book.api.views.helper.helper import new_psw
from school_book.api.views.helper.helper import now
from school_book.api.config import db

class User(db.Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    unique_ID = Column(Unicode(255), unique=True, default='')
    first_name = Column(Unicode(255), nullable=False)
    last_name = Column(Unicode(255), nullable=False)
    email = Column(Unicode(255), nullable=False)
    parent_one = Column(Unicode(255), default=None)
    parent_two = Column(Unicode(255), default=None)
    activated = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey('role.id', ondelete='CASCADE'))
    password = Column(Unicode(255), nullable=False)
    salt = Column(Unicode(255), nullable=False)
    created = Column(DateTime, nullable=False, default=now())
    first_login = Column(DateTime, nullable=False, default=now())
    last_login = Column(DateTime, nullable=False, default=now())
    address = Column(Unicode(255), nullable=False)
    phone = Column(Unicode(255), nullable=False)

    role = relationship('Role')

    def __repr__(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

    def set_salt(self):
        self.salt = new_salt()

    def set_psw(self):
        self.password = new_psw(self.salt, self.password)


class Role(db.Model):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True)
    role_name = Column(Unicode(255), nullable=False)

    def __repr__(self):
        return '{0}'.format(self.role_name)
