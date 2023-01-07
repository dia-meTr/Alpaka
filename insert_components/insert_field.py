from base_classes.field import Field


class InsertField(Field):
    """
    class for every field of table
    """
    def __init__(self, root, my_cursor, table, field_name, type_, null, key, default, extra):

        super().__init__(root, my_cursor, table, field_name, type_, null, key, default, extra)

    def get_value(self):
        value = self.value.get()
        if self.extra == 'auto_increment':
            return None
        elif value == '' and self.default is not None:
            value = self.default
        elif value == '' and self.null == 0:
            raise Exception(f"Sorry, column '{self.field_name}' can't be NULL")
        elif value == '' and self.null != 0:
            value = None

        value = self.check_type(value)

        return self.field_name, value
