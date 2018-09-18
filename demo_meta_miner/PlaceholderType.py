import sqlalchemy.types as types


class PlaceholderType(types.UserDefinedType):
    """
    New sqlalchemy type for undefined values, used while creating table
    """
    def __init__(self):
        pass

    def get_col_spec(self, **kw):
        return "--PlaceholderType--"
