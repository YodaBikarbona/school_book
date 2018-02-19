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
from school_book.api.views.constants.constants import DEACTIVATED


class SchoolYear(db.Model):
    __tablename__ = 'school_year'

    id = Column(Integer, primary_key=True)
    start = Column(Integer, nullable=False)
    end = Column(Integer, nullable=False)

    def __repr__(self):
        return '{0}/{1}'.format(self.start, self.end)
