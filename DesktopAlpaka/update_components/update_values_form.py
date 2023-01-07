from DesktopAlpaka.update_components.update_field import UpdateField
from DesktopAlpaka.base_classes.values_form import ValuesForm


class UpdateValuesForm(ValuesForm):
    """
        This class inherits ValuesForm and override
        new_field method for Update needs
        """
    def __init__(self, root, my_cursor, table):
        super().__init__(root, my_cursor, table)

    def new_field(self, el):
        """
            method for creating new fields and then
            adding them to form
        """
        field = UpdateField(self, self.cursor, self.table, *el)
        return field
