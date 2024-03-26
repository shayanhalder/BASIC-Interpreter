from basic.variables import VariableStatement
from basic.token import GrinToken

class AddOperator(VariableStatement):
    """ Class representing the ADD statement. """
    def __init__(self, grin_tokens: list[GrinToken], current_line_number: int,
                 interpreter_variables: dict, label:str=None):

        super().__init__(grin_tokens, current_line_number, interpreter_variables, label)

    def execute_statement(self) -> tuple[int, bool]:
        """ Adds the value of the variable in the interpreter variables dictionary by the
            value specified, and returns 1 since the line number will always be incremented/move
            forward (no control flow)."""

        with super().CatchErrors(line_change = 1) as execution_result:
            current_value = self._interpreter_variables.get(self._variable_name, 0)

            if type(current_value) is str and type(self._new_value) is not str or \
                type(current_value) is not str and type(self._new_value) is str:

                raise ValueError("Cannot add string literals to numbers")
            elif type(current_value) is str and type(self._new_value) is str:
                variable_sum = current_value + self._new_value
            elif type(current_value) is float or type(self._new_value) is float:
                variable_sum = float(current_value) + float(self._new_value)
            else:
                variable_sum = current_value + self._new_value

            self._interpreter_variables[self._variable_name] = variable_sum

        return execution_result.get_result()


class SubtractOperator(VariableStatement):
    """ Class representing the SUB statement. """
    def __init__(self, grin_tokens: list[GrinToken], current_line_number: int,
                 interpreter_variables: dict, label:str=None):

        super().__init__(grin_tokens, current_line_number, interpreter_variables, label)

    def execute_statement(self) -> tuple[int, bool]:
        """ Subtracts the value of the variable in the interpreter variables dictionary by the
            value specified, and returns 1 since the line number will always be incremented/move
            forward (no control flow)."""

        with super().CatchErrors(line_change = 1) as execution_result:
            current_value = self._interpreter_variables.get(self._variable_name, 0)

            if type(current_value) is str or type(self._new_value) is str:

                raise ValueError("Cannot subtract string literals")
            elif type(current_value) is float or type(self._new_value) is float:
                variable_difference = float(current_value) - float(self._new_value)
            else:
                variable_difference = current_value - self._new_value

            self._interpreter_variables[self._variable_name] = variable_difference

        return execution_result.get_result()

class MultiplicationOperator(VariableStatement):
    """ Class representing the MULT statement. """
    def __init__(self, grin_tokens: list[GrinToken], current_line_number: int,
                 interpreter_variables: dict, label: str = None):

        super().__init__(grin_tokens, current_line_number, interpreter_variables, label)

    def execute_statement(self) -> tuple[int, bool]:
        """ Multiplies the value of the variable in the interpreter variables dictionary by the
            value specified, and returns 1 since the line number will always be incremented/move
            forward (no control flow)."""

        with super().CatchErrors(line_change = 1) as execution_result:
            current_value = self._interpreter_variables.get(self._variable_name, 0)

            if type(current_value) is str and type(self._new_value) is float or \
                    type(current_value) is float and type(self._new_value) is str:

                raise ValueError("Cannot multiply string literals by floats")

            elif type(current_value) is str and type(self._new_value) is int and self._new_value < 0 \
                or type(current_value) is int and current_value < 0 and type(self._new_value) is str:
                raise ValueError("Cannot multiply string literals by negative integers")

            variable_product = current_value * self._new_value

            self._interpreter_variables[self._variable_name] = variable_product

        return execution_result.get_result()


class DivisionOperator(VariableStatement):
    """ Class representing the DIV statement. """
    def __init__(self, grin_tokens: list[GrinToken], current_line_number: int,
                 interpreter_variables: dict, label: str = None):

        super().__init__(grin_tokens, current_line_number, interpreter_variables, label)

    def execute_statement(self) -> tuple[int, bool]:
        """ Divides the value of the variable in the interpreter variables dictionary by the
            value specified, and returns 1 since the line number will always be incremented/move
            forward (no control flow)."""

        with super().CatchErrors(line_change = 1) as execution_result:
            current_value = self._interpreter_variables.get(self._variable_name, 0)

            if type(current_value) is str or type(self._new_value) is str:

                raise ValueError("Cannot divide by string literals")
            elif self._new_value == 0:
                raise ValueError("Cannot divide by zero")
            elif type(current_value) is int and type(self._new_value) is int:
                variable_quotient = int(current_value / self._new_value)
            else: # type(current_value) is float or type(current_value) is float:
                variable_quotient = current_value / self._new_value

            self._interpreter_variables[self._variable_name] = variable_quotient

        return execution_result.get_result()



