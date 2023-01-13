"""This is module for fields class for updating purposes"""
from values_form.field import Field
from base_classes.Error import MySQLError


class UpdateField(Field): # pylint: disable=too-many-ancestors
    """class for every field of table for updating purposes"""

    def get_value(self):
        """This is method for getting a pair of field name and its value"""
        value = self.value.get()
        if value == '':
            return None
        if self.key == 'MUL' and int(value) not in self.referenced_to:
            raise MySQLError(f"Sorry, column '{self.field_name}' has incorrect value")

        value = self.check_type(value)

        return self.field_name, value
