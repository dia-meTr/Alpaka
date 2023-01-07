from DesktopAlpaka.base_classes.field import Field


class UpdateField(Field):
    def __init__(self, root, my_cursor, table, field_name, type_, null, key, default, extra):
        super().__init__(root, my_cursor, table, field_name, type_, null, key, default, extra)

    def get_value(self):
        value = self.value.get()
        if value == '':
            return None
        else:
            value = self.check_type(value)

        return self.field_name, value
