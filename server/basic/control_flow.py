from basic.statements import Statement
from basic.token import GrinToken, GrinTokenKind
from basic.relational_operators import LessThanOperator, EqualToOperator

class ControlFlow(Statement):
    """ Base classes for all control flow statements to inherit from, namely GOTO and GOSUB. """
    def __init__(self, grin_tokens: list[GrinToken], current_line_number: int, max_line_number: int,
                 interpreter_variables: dict, label:str=None, interpreter_labels:dict=None):
        super().__init__(grin_tokens, current_line_number, label)
        self._interpreter_variables = interpreter_variables
        self._interpreter_labels = interpreter_labels
        self._target_token = grin_tokens[1]
        self._max_line_number = max_line_number
        if len(grin_tokens) == 6:
            self._conditional_expression = grin_tokens[3:]
        else:
            self._conditional_expression = None

    def evaluate_conditional_expression(self) -> bool:
        """ Method to evaluate the conditional expression in the control flow statement. """
        if self._conditional_expression is None:
            return True # control flow will always be modified if there is no conditional

        operation = self._conditional_expression[1]
        if operation.kind() is GrinTokenKind.LESS_THAN:
            return (LessThanOperator(*self._conditional_expression, interpreter_variables = self._interpreter_variables)
                    .evaluate_expression())
        elif operation.kind() is GrinTokenKind.LESS_THAN_OR_EQUAL:
            return LessThanOperator(*self._conditional_expression,
                                    interpreter_variables = self._interpreter_variables).evaluate_expression() or \
                    EqualToOperator(*self._conditional_expression,
                                    interpreter_variables = self._interpreter_variables).evaluate_expression()
        elif operation.kind() is GrinTokenKind.EQUAL:
            return EqualToOperator(*self._conditional_expression,
                                   interpreter_variables = self._interpreter_variables).evaluate_expression()
        elif operation.kind() is GrinTokenKind.GREATER_THAN:
            return not (LessThanOperator(*self._conditional_expression,
                                         interpreter_variables = self._interpreter_variables).evaluate_expression() or
                    EqualToOperator(*self._conditional_expression,
                                    interpreter_variables = self._interpreter_variables).evaluate_expression())
        elif operation.kind() is GrinTokenKind.GREATER_THAN_OR_EQUAL:
            return not LessThanOperator(*self._conditional_expression,
                                        interpreter_variables = self._interpreter_variables).evaluate_expression()
        elif operation.kind() is GrinTokenKind.NOT_EQUAL:
            return not EqualToOperator(*self._conditional_expression,
                                       interpreter_variables = self._interpreter_variables).evaluate_expression()

    def execute_statement(self) -> tuple[int, bool]:
        """ All base classes (GOTO and GOSUB) will have their own implementation of the
            execute_statement() method. """
        pass


class GoToStatement(ControlFlow):
    """ Class implementing the GOTO statement in GRIN. """
    def __init__(self, grin_tokens: list[GrinToken], current_line_number: int, max_line_number: int,
                 interpreter_variables: dict, label:str=None, interpreter_labels:dict=None):

        super().__init__(grin_tokens, current_line_number, max_line_number,
                 interpreter_variables, label, interpreter_labels)


    def execute_statement(self) -> tuple[int, bool]:
        """ Returns an integer with the line change as a result of the GOTO statement, as well as
            a boolean expression indicating whether the program will continue or not. """
        with super().CatchErrors() as execution_result:
            if self.evaluate_conditional_expression(): # execute statement if conditional is true
                if self._target_token.kind() is GrinTokenKind.IDENTIFIER: # variable used
                    # get value of the variable if used, and remove quotes from string
                    variable_value = str(self._interpreter_variables.get(self._target_token.text().replace('"',''), '0'))
                else: # get value of the literal string or integer
                    variable_value = self._target_token.text()

                if variable_value.strip().replace('-', '').isnumeric(): # it is integer
                    line_number_change = int(variable_value)
                    target_line_number = self.get_current_line_number() + line_number_change
                    if target_line_number < 0: # you can jump back to first line, but not before
                        raise ValueError("Target line number must be greater than zero")
                    elif target_line_number >= self._max_line_number:
                        raise ValueError("Target line number must be within the maximum line number")
                    elif line_number_change == 0:
                        raise ValueError("Cannot jump to the same line")
                    execution_result._line_change = line_number_change
                else: # it is string
                    variable_value = variable_value.replace('"', "")
                    target_line_number = self._interpreter_labels.get(variable_value, -1) # get line number associated with label
                    if target_line_number == -1: # label does not exist
                        raise ValueError("Non-existent label provided as target")
                    line_number_change = target_line_number - self.get_current_line_number()
                    execution_result._line_change = line_number_change
            else:
                line_number_change = 1 # if conditional false, we just move on to the next line
                execution_result._line_change = line_number_change

        return execution_result.get_result()



class GoSubStatement(GoToStatement):
    """ Class representing the GOSUB statement in Grin. All features identical to GOTO statement
        except that GOSUB statement adds the current_line + 1 to the gosub_callstack list
        in the interpreter. """
    def __init__(self, grin_tokens: list[GrinToken], current_line_number: int, max_line_number: int,
                 interpreter_variables: dict, call_stack: list, label:str=None, interpreter_labels:dict=None):
        super().__init__(grin_tokens, current_line_number, max_line_number,
                         interpreter_variables, label, interpreter_labels)
        call_stack.append(current_line_number + 1)
        self._call_stack = call_stack





