
class MySQLError(Exception):
    """Exception raised for errors with SQL request

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Oops, it's seems something goes wrong"):
        self.message = message
        super().__init__(self.message)
