import sqlalchemy.types as types


class PlaceholderType(types.UserDefinedType):
    def __init__(self):
        # self.precision = precision
        pass

    def get_col_spec(self, **kw):
        return "--PlaceholderType--"

    def bind_processor(self, dialect):
        def process(value):
            return value
        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            return value
        return process
