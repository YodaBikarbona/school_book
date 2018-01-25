from sqlalchemy import Column


class User:

    @classmethod
    def hello(cls):
        print('This is hello method')
