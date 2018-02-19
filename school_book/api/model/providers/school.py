from school_book.api.model.model.school import SchoolYear


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
        return ('a')