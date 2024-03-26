from basic.token import GrinToken, GrinTokenKind

class RelationalOperator: # doesn't inherit from Statement because it's a part of a GOTO/GOSUB statement
    """ Base class for all the relational operators to inherit from. """
    def __init__(self, value1: GrinToken, operation: GrinToken, value2: GrinToken, interpreter_variables: dict):
        self._interpreter_variables = interpreter_variables
        self._value1 = self._extract_values(value1)
        self._value2 = self._extract_values(value2)
        self._operation = operation

    def _extract_values(self, value: GrinToken):
        """ Extracts the values from both operands. """

        if value.kind() is GrinTokenKind.IDENTIFIER:
            return str(self._interpreter_variables.get(value.text(), 0))
        else:
            return value.text()

    def _validate_operands(self):
        """ Validates the types of the operands provided, raising errors if needed. """

        if (self._value1.replace('.', '').replace('-', '').isnumeric() and
            self._value2.isalpha()) or (self._value1.isalpha()
            and self._value2.replace('.', '').replace('-', '').isnumeric()):
            raise ValueError("Cannot use relational operator between string literal and number")

        return (self._extract_values_from_string(self._value1),
                self._extract_values_from_string(self._value2))

    def _extract_values_from_string(self, value: str):
        """ Extracts numbers from string if string is solely a number, otherwise returns
            the string value. """

        if value.replace('.', '').replace('-', '').isnumeric():
            return float(value)
        else:
            return value.replace('"', '')

    def evaluate_expression(self) -> bool:
        """ Method to return a boolean based on the value of the expression, will be
            implemented by base classes. """
        pass

class LessThanOperator(RelationalOperator):
    """ Class to represent the < (less than) relational operator in GRIN. """
    def __init__(self, value1: GrinToken, operation: GrinToken, value2: GrinToken, interpreter_variables: dict):
        super().__init__(value1, operation, value2, interpreter_variables)

    def evaluate_expression(self) -> bool:
        """ Returns a boolean based on the value of the expression. """
        value1, value2 = self._validate_operands()
        return value1 < value2

class EqualToOperator(RelationalOperator):
    """ Class to represent the = (equal to) relational operator in GRIN. """
    def __init__(self, value1: GrinToken, operation: GrinToken, value2: GrinToken, interpreter_variables: dict):
        super().__init__(value1, operation, value2, interpreter_variables)

    def evaluate_expression(self) -> bool:
        """ Returns a boolean based on the value of the expression. """
        value1, value2 = self._validate_operands()
        return value1 == value2



