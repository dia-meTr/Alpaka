"""
This is module for overriding
ValuesForm for Update needs
"""
from tabs.update_components.update_field import UpdateField
from values_form_components.values_form import ValuesForm


class UpdateValuesForm(ValuesForm):  # pylint: disable=too-many-ancestors
    """
    This class inherits ValuesForm and override
    new_field method for Update needs
    """

    def new_field(self, field_info):
        """
        This is method for creating new fields and then
        adding them to form
        """
        field = UpdateField(self, self.cursor, self.table, field_info)
        return field
