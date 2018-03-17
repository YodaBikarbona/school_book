from school_book.api.model.model.school import SchoolYear
from school_book.api.model.model.school import SchoolClass
from school_book.api.model.model.school import SchoolClassStudent
from school_book.api.model.model.school import SchoolSubject
from school_book.api.model.model.school import SchoolClassProfessor
from school_book.api.model.model.school import SchoolClassSubject
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
    def get_all_classes_by_school_year_id(cls, school_year_id, role_id=None):
        school_class = SchoolClass.query.filter(SchoolClass.school_year_id == school_year_id)
        if role_id:
            school_class = school_class.join(SchoolClassProfessor, SchoolClass.id == SchoolClassProfessor.classes_id)\
                .filter(SchoolClassProfessor.classes_id == role_id)

        return school_class.all()


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
    def get_all_subjects_by_class_id(cls, class_id):
        subjects = SchoolSubject.query.join(SchoolClassSubject, SchoolSubject.id == SchoolClassSubject.school_subject_id) \
            .filter(SchoolClassSubject.classes_id == class_id).all()
        return subjects


    @classmethod
    def get_professor_by_class_id(cls, class_id):
        return User.query.join(SchoolClassProfessor, User.id == SchoolClassProfessor.professor_id)\
            .filter(SchoolClassProfessor.classes_id == class_id).first()


    @classmethod
    def get_student_ids_by_class_id(cls, class_id):
        students = []
        temp_list = User.query.join(SchoolClassStudent, User.id == SchoolClassStudent.student_id) \
            .filter(SchoolClassStudent.classes_id == class_id).all()
        for student in temp_list:
            students.append(student.id)
        return students

    @classmethod
    def get_subject_ids_by_class_id(cls, class_id):
        subjects = []
        temp_list = SchoolSubject.query.join(SchoolClassSubject,
                                             SchoolSubject.id == SchoolClassSubject.school_subject_id) \
            .filter(SchoolClassSubject.classes_id == class_id).all()
        for subject in temp_list:
            subjects.append(subject.id)
        return subjects

    @classmethod
    def get_class_subject_by_id(cls, subject_id, class_id):
        class_subject = SchoolClassSubject.query.filter(SchoolClassSubject.school_subject_id == subject_id,
                                                        SchoolClassSubject.classes_id == class_id).first()
        return class_subject

    @classmethod
    def get_class_subjects_by_class_id(cls, class_id):
        class_subjects = SchoolSubject.query.join(SchoolClassSubject,
                                                  SchoolSubject.id == SchoolClassSubject.school_subject_id) \
            .filter(SchoolClassSubject.classes_id == class_id).all()
        return class_subjects

    @classmethod
    def get_class_student_by_id(cls, student_id, class_id):
        class_student = SchoolClassStudent.query.filter(SchoolClassStudent.student_id == student_id,
                                                        SchoolClassStudent.classes_id == class_id).first()
        return class_student
