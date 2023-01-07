from update_components.update_field import UpdateField
from base_classes.values_form import ValuesForm


class UpdateValuesForm(ValuesForm):
    def __init__(self, root, my_cursor, table):
        super().__init__(root, my_cursor, table)

    def new_field(self, el):
        field = UpdateField(self, self.cursor, self.table, *el)
        return field
