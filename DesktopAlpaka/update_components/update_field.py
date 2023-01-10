"""This is module for fields class for updating purposes"""
from base_classes.field import Field
from base_classes.Error import MySQLError


class UpdateField(Field):

    def get_value(self):
        """This is method for getting a pair of field name and its value"""
        value = self.value.get()
        if value == '':
            return None
        if self.key == 'MUL' and int(value) not in self.referenced_to:
            raise MySQLError(f"Sorry, column '{self.field_name}' has incorrect value")
        else:
            value = self.check_type(value)

        return self.field_name, value
