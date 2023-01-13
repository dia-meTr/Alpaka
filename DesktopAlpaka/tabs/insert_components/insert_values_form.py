"""
This is module for overriding
ValuesForm for Insert needs
"""
from tabs.insert_components.insert_field import InsertField
from values_form_components.values_form import ValuesForm


class InsertValuesForm(ValuesForm):  # pylint: disable=too-many-ancestors
    """
    This class inherits ValuesForm and override
    new_field method for Insert needs
    """
    def new_field(self, field_info):
        """
        method for creating new fields and then
        adding them to form
        """
        field = InsertField(self, self.cursor, self.table, field_info)
        return field
