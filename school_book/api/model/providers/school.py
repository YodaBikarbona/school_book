from school_book.api.model.model.school import SchoolYear
from school_book.api.model.model.school import SchoolClass
from school_book.api.model.model.school import SchoolClassStudent
from school_book.api.model.model.school import SchoolSubject
from school_book.api.model.model.school import SchoolClassProfessor
from school_book.api.model.model.user import User


class SchoolProvider:

    @classmethod
    def get_school_year(cls, start, end):
        return SchoolYear.query.filter(SchoolYear.start == start,
                                       SchoolYear.end == end).first()


    @classmethod
    def get_all_school_years(cls):
        return SchoolYear.query.all()


    @classmethod
    def get_all_classes_by_school_year_id(cls, school_year_id):
        return SchoolClass.query.filter(SchoolClass.school_year_id == school_year_id).all()


    @classmethod
    def get_number_of_students(cls, class_id):
        return SchoolClassStudent.query.filter(SchoolClassStudent.classes_id == class_id).count()


    @classmethod
    def get_all_school_subjects(cls):
        return SchoolSubject.query.all()


    @classmethod
    def get_all_students_by_class_id(cls, class_id):
        students = User.query.join(SchoolClassStudent, User.id == SchoolClassStudent.student_id)\
            .filter(SchoolClassStudent.classes_id == class_id).all()
        return students


    @classmethod
    def get_professor_by_class_id(cls, class_id):
        return User.query.join(SchoolClassProfessor, User.id == SchoolClassProfessor.professor_id)\
            .filter(SchoolClassProfessor.classes_id == class_id).first()
