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
from school_book.api.model.model.user import User


class SchoolYear(db.Model):
    __tablename__ = 'school_year'

    id = Column(Integer, primary_key=True)
    start = Column(Integer, nullable=False)
    end = Column(Integer, nullable=False)

    def __repr__(self):
        return '{0}/{1}'.format(self.start, self.end)


class SchoolClass(db.Model):
    __tablename__ = 'classes'

    id = Column(Integer, primary_key=True)
    name = Column(Integer, nullable=False)
    school_year_id = Column(Integer, ForeignKey('school_year.id', ondelete='CASCADE'))

    school_year = relationship('SchoolYear')

    def __repr__(self):
        return '{0}'.format(self.name)


class SchoolClassStudent(db.Model):
    __tablename__ = 'classes_student'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    classes_id = Column(Integer, ForeignKey('classes.id', ondelete='CASCADE'))

    classes = relationship('SchoolClass')
    user = relationship('User')

    def __repr__(self):
        return '{0} {1}'.format(self.user.first_name, self.user.last_name)


class SchoolClassProfessor(db.Model):
    __tablename__ = 'classes_professor'

    id = Column(Integer, primary_key=True)
    multiple_professors = Column(Boolean, default=False)
    professor_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    classes_id = Column(Integer, ForeignKey('classes.id', ondelete='CASCADE'))

    classes = relationship('SchoolClass')
    user = relationship('User')

    def __repr__(self):
        return '{0} {1}'.format(self.user.first_name, self.user.last_name)


class SchoolSubject(db.Model):
    __tablename__ = 'school_subjects'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), nullable=False)
    professor_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))

    user = relationship('User')

    def __repr__(self):
        return '{0}'.format(self.name)


class SchoolClassSubject(db.Model):
    __tablename__ = 'classes_school_subject'

    id = Column(Integer, primary_key=True)
    school_subject_id = Column(Integer, ForeignKey('school_subjects.id', ondelete='CASCADE'))
    classes_id = Column(Integer, ForeignKey('classes.id', ondelete='CASCADE'))

    classes = relationship('SchoolClass')
    subjects = relationship('SchoolSubject')

    def __repr__(self):
        return '{0} {1}'.format(self.subjects.name)


class Absence(db.Model):
    __tablename__ = 'absences'

    id = Column(Integer, primary_key=True)
    class_id = Column(Integer, ForeignKey('classes.id', ondelete='CASCADE'))
    school_subject_id = Column(Integer, ForeignKey('school_subjects.id', ondelete='CASCADE'))
    professor_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    student_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    date = Column(DateTime, nullable=True, default=now())
    comment = Column(Unicode(255), nullable=True)

    classes = relationship('SchoolClass')
    subjects = relationship('SchoolSubject')
    user_professor = relationship('User', foreign_keys=[professor_id])
    user_student = relationship('User', foreign_keys=[student_id])

    def __repr__(self):
        return '{0} {1}'.format(self.user.first_name, self.user.last_name)


class Grade(db.Model):
    __tablename__ = 'grades'

    id = Column(Integer, primary_key=True)
    class_id = Column(Integer, ForeignKey('classes.id', ondelete='CASCADE'))
    school_subject_id = Column(Integer, ForeignKey('school_subjects.id', ondelete='CASCADE'))
    professor_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    student_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    date = Column(DateTime, nullable=True, default=now())
    comment = Column(Unicode(255), nullable=True)
    grade = Column(Integer, nullable=False)

    classes = relationship('SchoolClass')
    subjects = relationship('SchoolSubject')
    user_professor = relationship('User', foreign_keys=[professor_id])
    user_student = relationship('User', foreign_keys=[student_id])

    def __repr__(self):
        return '{0} {1}'.format(self.user.first_name, self.user.last_name)
