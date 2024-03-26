from basic.statements import Statement
from basic.token import GrinToken, GrinTokenKind

class PrintStatement(Statement):
    """ Class representing the PRINT statement in GRIN. """
    def __init__(self, grin_tokens: list[GrinToken], current_line_number: int,
                 interpreter_variables: dict, label:str=None):
        super().__init__(grin_tokens, current_line_number, label)

        # extract proper type from value provided to PRINT statement
        if grin_tokens[1].kind() is GrinTokenKind.LITERAL_STRING:
            self._print_value = grin_tokens[1].text().replace('"', "") # remove quotation marks
        elif grin_tokens[1].kind() is GrinTokenKind.LITERAL_INTEGER:
            self._print_value = int(grin_tokens[1].text())
        elif grin_tokens[1].kind() is GrinTokenKind.LITERAL_FLOAT:
            self._print_value = float(grin_tokens[1].text())
        elif grin_tokens[1].kind() is GrinTokenKind.IDENTIFIER: # variable is used in print statement
            variable_name = grin_tokens[1].text()
            self._print_value = interpreter_variables.get(variable_name, 0) # default to 0

    def get_print_value(self) -> str:
        """ Returns the value that will be printed by the PRINT statement. """
        return self._print_value

    def execute_statement(self) -> tuple[int, bool]:
        """ Prints the value of the PRINT statement to the console, raising an error if a
            newline is given. """

        with super().CatchErrors(line_change = 1) as execution_result:
            if type(self._print_value) is str and self._print_value.find("\\n") != -1:
                raise ValueError("Cannot have newline characters (\\n) in string literal")
            else:
                print(self._print_value)

        return execution_result.get_result()




