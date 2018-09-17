import sqlalchemy.types as types


class PlaceholderType(types.UserDefinedType):
    """New sqlalchemy type for undefined values, used while creating table"""
    def __init__(self):
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
