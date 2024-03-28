import basic
from flask import Flask, request, jsonify
from flask_cors import CORS
import contextlib
from flask_socketio import SocketIO
import io
import json

app = Flask(__name__)
CORS(app, origins='*')
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/', methods=['GET'])
def hello_world():
    print('home page')
    return 'Hello from Flask!'
    
@socketio.on('connect')
def greet():
    print('Flask Server established socket connection with client')

@socketio.on('continue-execution')
def continue_execution(obj):
    parsed_data = json.loads(obj.replace("\n", "\\n"))
    interpreter_state = parsed_data['body']
    parsed_input_code = interpreter_state['lines'].split("\n")
    tokens = get_tokens(parsed_input_code)
    
    print(interpreter_state)
    
    if tokens is not None:
        with contextlib.redirect_stdout(io.StringIO()) as output:
            interpreter = basic.Interpreter(tokens, socketio)
            interpreter._current_line = interpreter_state['current_line']
            interpreter._variables = interpreter_state['variables']
            interpreter._labels = interpreter_state['labels']
            interpreter._gosub_callstack = interpreter_state['callstack']
            interpreter._user_inputs.append(interpreter_state['user_input'])
            interpreter._current_output = interpreter_state['output']
            
            final_state = interpreter.run()

        output_code = output.getvalue()
        print('final state', final_state)
        final_state['output'] += output_code
        final_state['lines'] = interpreter_state['lines']
        
        if not final_state['paused']:
            socketio.emit('execution-finished', final_state)
        else: # we are paused
            socketio.emit('input-event', final_state)


@socketio.on('run-interpreter')
def greet_client(body: str):
    print('running interpreter')
    print('received input code: ')
    print(body)
    body = json.loads(body.replace("\n", "\\n"))
    
    input_code = body['body']
    parsed_input = input_code.split("\n")
    
    tokens = get_tokens(parsed_input)
    if tokens is not None:
        with contextlib.redirect_stdout(io.StringIO()) as output:
            interpreter = basic.Interpreter(tokens, socketio)
            final_state = interpreter.run()
            
            
        output_code = output.getvalue()
        print('final state', final_state)
        final_state['output'] = output_code
        final_state['lines'] = input_code
        
        if not final_state['paused']:
            socketio.emit('execution-finished', final_state)
        else: # we are paused
            socketio.emit('input-event', final_state)
    

def get_tokens(grin_code: list[str]) -> list[list[basic.GrinToken]] | None:
    """ Given a list of strings representing lines of GRIN code, it returns
        a parsed list of grin tokens. """
    try:
        return list(basic.parse(grin_code))
    except Exception as error:
        print(f'GrinError: {error}')
        return None

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port='3002')

