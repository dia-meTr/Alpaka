"""This is module for fields class for inserting purposes"""
from base_classes.field import Field
from base_classes.Error import MySQLError


class InsertField(Field):  # pylint: disable=too-many-ancestors
    """class for every field of table"""

    def get_value(self):
        """This is method for getting a pair of field name and its value"""
        value = self.value.get()
        if self.extra == 'auto_increment':
            return None
        if value == '' and self.default is not None:
            value = self.default
        elif value == '' and self.null == 0:
            raise MySQLError(f"Sorry, column '{self.field_name}' can't be NULL")
        elif value == '' and self.null != 0:
            value = None
        elif self.key == 'MUL' and int(value) not in self.referenced_to:
            raise MySQLError(f"Sorry, column '{self.field_name}' has incorrect value")

        value = self.check_type(value)

        return self.field_name, value
