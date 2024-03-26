from basic.statements import Statement
from basic.token import GrinToken

class UserInput(Statement):
    """ Base class for all statements collecting user input, namely INNUM and INSTR. """
    def __init__(self, grin_tokens: list[GrinToken], current_line_number: int,
                 interpreter_variables: dict, label:str=None, test_input:str=None):

        super().__init__(grin_tokens, current_line_number, label)
        self._interpreter_variables = interpreter_variables
        self._variable_stored = grin_tokens[1].text()
        self._test_input = test_input

    def _read_input(self):
        """ Reads the user input, but if in unit-testing mode, it uses the parameter from the
            constructor. """

        if self._test_input:
            self._user_input = self._test_input
        else: # cannot test line below because it requires us to redirect standard input, which we didn't learn
            self._user_input = input()

    def execute_statement(self) -> tuple[int, bool]:
        """ Implemented in base classes. """
        pass


class InputNumber(UserInput):
    """ Class representing the INNUM statement in Grin. """
    def __init__(self, grin_tokens: list[GrinToken], current_line_number: int,
                 interpreter_variables: dict, label:str=None, test_input:str=None):

        super().__init__(grin_tokens, current_line_number, interpreter_variables, label, test_input)

    def execute_statement(self) -> tuple[int, bool]:
        """ Prompt user for input value and store in the corresponding variable. """

        with (super().CatchErrors(line_change = 1) as execution_result):
            self._read_input()
            if not self._user_input.strip().replace(".", "").replace("-", "").isnumeric():
                raise ValueError("INNUM cannot read string literal")

            # .isdigit() returns True if there are no decimals in the string.
            variable_value = int(self._user_input) if self._user_input.strip().replace("-","").isdigit() \
                                else float(self._user_input)

            # store the user input value in the corresponding variable
            self._interpreter_variables[self._variable_stored] = variable_value

        return execution_result.get_result()

class InputString(UserInput):
    """ Class representing the INSTR statement in Grin. """
    def __init__(self, grin_tokens: list[GrinToken], current_line_number: int,
                 interpreter_variables: dict, label:str=None, test_input:str=None):

        super().__init__(grin_tokens, current_line_number, interpreter_variables, label, test_input)

    def execute_statement(self) -> tuple[int, bool]:
        """ Prompt user for input value and store in the corresponding variable. """
        with super().CatchErrors(line_change = 1) as execution_result:
            self._read_input()
            self._interpreter_variables[self._variable_stored] = self._user_input

        return execution_result.get_result()







