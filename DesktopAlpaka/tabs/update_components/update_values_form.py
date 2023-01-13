"""
This is module for overriding
ValuesForm for Update needs
"""
from tabs.update_components.update_field import UpdateField
from values_form.values_form import ValuesForm


class UpdateValuesForm(ValuesForm):
    """
    This class inherits ValuesForm and override
    new_field method for Update needs
    """
    def __init__(self, root, my_cursor, table):
        super().__init__(root, my_cursor, table)

    def new_field(self, el):
        """
        This is method for creating new fields and then
        adding them to form
        """
        field = UpdateField(self, self.cursor, self.table, el)
        return field
