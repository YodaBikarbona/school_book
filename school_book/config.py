from school_book.api.model.model.config import Base
from school_book.api.model.model.config import engine
from school_book.api.config import app


def init_db():
    Base.metadata.create_all(bind=engine)


def main():
    if __name__ == '__main__':
        app.run(debug=True, port=8080)
