

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

# @app.route('/interpreter', methods=['POST'])
# def get_output():
#     print('LOG: Getting BASIC output from interpreter. ')

#     article_info = request.json
#     input_code = article_info['body']
#     parsed_input = input_code.split("\n") 

#     tokens = get_tokens(parsed_input)
#     if tokens is not None:
#         with contextlib.redirect_stdout(io.StringIO()) as output:
#             interpreter = basic.Interpreter(tokens, socketio)
#             interpreter.run()
        
#         output_code = output.getvalue()
#         return output_code
#     else:
#         return "error"
    
@socketio.on('connect')
def greet():
    print('connected to client')

@socketio.on('run-interpreter')
def greet_client(body: str):
    print('running interpreter')
    print('received input code: ')
    print(body)
    body = json.loads(body.replace("\n", "\\n"))
    print(type(body))
    
    input_code = body['body']
    parsed_input = input_code.split("\n")
    
    tokens = get_tokens(parsed_input)
    if tokens is not None:
        with contextlib.redirect_stdout(io.StringIO()) as output:
            interpreter = basic.Interpreter(tokens, socketio)
            interpreter.run()
        
        output_code = output.getvalue()
        return output_code
    else:
        return "error"
    

def get_tokens(grin_code: list[str]) -> list[list[basic.GrinToken]] | None:
    """ Given a list of strings representing lines of GRIN code, it returns
        a parsed list of grin tokens. """
    try:
        return list(basic.parse(grin_code))
    except Exception as error:
        print(f'GrinError: {error}')
        return None

if __name__ == "__main__":
    # app.run(debug=True, host="0.0.0.0", port='3002')
    socketio.run(app, debug=True, host="0.0.0.0", port='3002')

