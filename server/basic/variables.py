from basic.statements import Statement
from basic.token import GrinToken, GrinTokenKind

class VariableStatement(Statement):
    """ Class representing all statements changing or setting values to variables.
        By default, VariableStatement will override/set the value of a variable (LET statement), but
        arithmetic operators will inherit and can cause operations to be done on the variable. """

    def __init__(self, grin_tokens: list[GrinToken], current_line_number: int,
                 interpreter_variables: dict, label:str|None=None):

        super().__init__(grin_tokens, current_line_number, label)
        self._variable_name = grin_tokens[1].text()

        if grin_tokens[2].kind() is GrinTokenKind.IDENTIFIER:
            string = grin_tokens[2].text()
            self._new_value = interpreter_variables.get(string, 0)
        else:
            if grin_tokens[2].kind() is GrinTokenKind.LITERAL_STRING:
                string = grin_tokens[2].text().replace('"', "")
                self._new_value = string
            elif grin_tokens[2].kind() is GrinTokenKind.LITERAL_INTEGER:
                self._new_value = int(grin_tokens[2].text())
            elif grin_tokens[2].kind() is GrinTokenKind.LITERAL_FLOAT:
                self._new_value = float(grin_tokens[2].text())

        self._interpreter_variables = interpreter_variables


    def execute_statement(self) -> tuple[int, bool]:
        """ Sets the value of the variable in the interpreter variables dictionary, and
            returns 1 since the line number will always be incremented/move forward (no control flow)."""

        with super().CatchErrors(line_change = 1) as execution_result:
            if type(self._new_value) is str and self._new_value.find("\\n") != -1:
                raise ValueError("Cannot have newline characters (\\n) in string literal")
            self._interpreter_variables[self._variable_name] = self._new_value

        return execution_result.get_result()


    


