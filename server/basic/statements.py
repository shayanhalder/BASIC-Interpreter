from basic.token import GrinToken

class CatchGrinErrors:
    """ Custom Context Manager for catching any run-time errors that are raised while
        executing any Grin Statement, in which case they are printed to the shell automatically. """
    def __init__(self, line_change: int=None):
        self._line_change = line_change
        self._continue_program = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type is None or exc_value is None:
            pass
        else:
            print(f'GrinError: {exc_value}')
            self._continue_program = False
            return True

    def get_result(self) -> tuple[int, bool]:
        """ Returns the line number change after executing the program and whether
            or not the program will continue executing (if error was/wasn't raised)."""

        return self._line_change, self._continue_program


class Statement:
    """ Base class for all statements to inherit from. """
    def __init__(self, grin_tokens: list[GrinToken], current_line_number: int, label: str):
        self._primary_keyword = grin_tokens[0].text()
        self._label = label
        self._line_number = current_line_number

    @staticmethod
    def CatchErrors(line_change: int=None) -> CatchGrinErrors:
        """ Returns a Context Manager to automatically catch and print any Grin Errors
            that occur at run-time. """
        return CatchGrinErrors(line_change)

    def get_label(self) -> str:
        """ Returns the label associated with the statement, otherwise None if no label. """
        return self._label

    def get_current_line_number(self) -> int:
        """ Returns the line number associated with the statement. """
        return self._line_number

    def primary_keyword(self) -> str:
        """ Returns the primary keyword string of the statement. """
        return self._primary_keyword

    def execute_statement(self) -> tuple[int, bool]:
        """ Executes the statement, updating the program's state (e.g line number, variables, etc...).
            Returns the line number of the program after this statement is executed. Method left
            blank as it will be implemented differently by all subclasses of Statement. """

        pass






