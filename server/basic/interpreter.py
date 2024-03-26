from basic.token import GrinToken, GrinTokenKind
import basic.variables, basic.printing, basic.arithmetic_operators, basic.user_input, basic.control_flow
import flask_socketio

class Interpreter:
    """ Class that runs through each list of tokens given from the user input's grin code
        and executes / evaluates each statement, printing any output."""

    def __init__(self, lines: list[list[GrinToken]], socket_connection: flask_socketio.SocketIO) -> None:
        self._lines = lines # each element is a list with the tokens in one line
        self._max_lines = len(lines)
        self._current_line = 0
        self._variables = dict()
        self._labels = dict()
        self._gosub_callstack = [] # contains all line numbers being remembered from GOSUB statements
        self._socketio = socket_connection

    def run(self) -> None:
        """ Runs the interpreter on the provided GRIN code from the user. """

        self._parse_label_lines(self._lines) # associate all labels with their line numbers

        while self._current_line < len(self._lines):
            current_line_tokens = self._lines[self._current_line]
            current_keyword = current_line_tokens[0] # every line starts with a keyword
            current_line_label = self._labels.get(current_keyword.text(), None)

            if current_keyword.kind() is GrinTokenKind.END:
                break  # don’t need to worry about ‘.’, parser already excludes it

            if current_keyword.kind() is GrinTokenKind.RETURN:
                if len(self._gosub_callstack) > 0: # must be in a subroutine to execute "RETURN" statement
                    self._current_line = self._gosub_callstack.pop()
                    continue
                else:
                    print("GrinError: RETURN statement reached while not in subroutine")
                    break

            if current_line_label is not None: # statement_tokens excludes any potential labels in the line
                statement_tokens = current_line_tokens[2:]
            else:
                statement_tokens = current_line_tokens

            line_number_change = self._execute_statement(statement_tokens, current_line_label)
            if line_number_change is None:
                break
            self._current_line += line_number_change

    def _execute_statement(self, current_line_tokens: list[GrinToken], label:str=None) -> int | None: # assumes no label in current_line_tokens
        """ Executes a line of GRIN code and returns an integer representing the change in the
            program's line number from its current one after executing the statement. """

        keyword = current_line_tokens[0]
        if keyword.kind() is GrinTokenKind.LET:
            statement = basic.variables.VariableStatement(current_line_tokens, self._current_line,
                                             self._variables, label)
        elif keyword.kind() is GrinTokenKind.PRINT:
            statement = basic.printing.PrintStatement(current_line_tokens, self._current_line,
                                             self._variables, label)

        elif keyword.kind() is GrinTokenKind.ADD:
            statement = basic.arithmetic_operators.AddOperator(current_line_tokens, self._current_line,
                                                     self._variables, label)

        elif keyword.kind() is GrinTokenKind.SUB:
            statement = basic.arithmetic_operators.SubtractOperator(current_line_tokens, self._current_line,
                                                     self._variables, label)

        elif keyword.kind() is GrinTokenKind.MULT:
            statement = basic.arithmetic_operators.MultiplicationOperator(current_line_tokens, self._current_line,
                                                     self._variables, label)

        elif keyword.kind() is GrinTokenKind.DIV:
            statement = basic.arithmetic_operators.DivisionOperator(current_line_tokens, self._current_line,
                                                     self._variables, label)

        # can't unit test INNUM and INSTR since that requires redirecting input, which we didn't learn
        elif keyword.kind() is GrinTokenKind.INNUM:
            flask_socketio.emit('input-event', 'innum triggered')    
            statement = basic.user_input.InputNumber(current_line_tokens, self._current_line,
                                                    self._variables, label, test_input=input)

        elif keyword.kind() is GrinTokenKind.INSTR:
            statement = basic.user_input.InputString(current_line_tokens, self._current_line,
                                                    self._variables, label)

        elif keyword.kind() is GrinTokenKind.GOTO:
            statement = basic.control_flow.GoToStatement(current_line_tokens, self._current_line, self._max_lines,
                                                    self._variables, label, self._labels)

        elif keyword.kind() is GrinTokenKind.GOSUB:
            statement = basic.control_flow.GoSubStatement(current_line_tokens, self._current_line, self._max_lines,
                                                    self._variables, self._gosub_callstack, label, self._labels)


        line_number_change, program_continuing = statement.execute_statement()

        # cannot test that a program will quit, but I DID test that error messages are raised
        if not program_continuing:
            return None

        return line_number_change

    def _parse_label_lines(self, line_tokens: list[list[GrinToken]]) -> None:
        """ Scans through the lists of tokens and associates any labels with their
            corresponding line number in the self._labels dictionary to be used
            in the future. """

        for index, line in enumerate(line_tokens):
            if line[0].kind() is GrinTokenKind.IDENTIFIER:
                label = line[0].text()
                self._labels[label] = index


