"""This is module for fields class for inserting purposes"""
from values_form_components.field import Field
from base_classes.error import MySQLError


class InsertField(Field):  # pylint: disable=too-many-ancestors
    """class for every field of table for inserting purposes"""

    def get_value(self):
        """This is method for getting a pair of field name and its value"""
        value = self.value.get()
        if self.extra == 'auto_increment':
            return None
        if value == '':
            self.no_value(value)
        elif self.key == 'MUL' and int(value) not in self.referenced_to:
            raise MySQLError(f"Sorry, column '{self.field_name}' has incorrect value")

        value = self.check_type(value)

        return self.field_name, value

    def no_value(self, value):
        """This is methode for setting value if its field empty"""
        if self.default is not None:
            value = self.default
        elif self.null == 0:
            raise MySQLError(f"Sorry, column '{self.field_name}' can't be NULL")
        elif self.null != 0:
            value = None
        return value
