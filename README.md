# BASIC-Interpreter

This is a full-stack web application primarily written in Python, which creates an interpreter for BASIC, a primitive high-level general purpose programming language used many decades ago.

## Tech Stack

React.js + Vite were used for the front-end, Python and Flask were used for the backend. Sockets were used to establish a continuous, bidirectional connection between the front-end and back-end in order to handle the fact that reading user input will momentarily halt the interpreter's execution. Socket events are used to allow the Python BASIC interpeter to halt execution until input from the React.js frontend is received.

## Interpreter Features

The interpreter currently supports statements for variable assigment, arithmetic operators, labels, relational operators, user input, control flow, subroutines, line labels / GOTO statements, and printing output. These statements were implemented in the interpreter using an object-oriented approach.

## Parsing

The interpreter lexes and parses the user input into tokens, which are used to allow the interpreter to disregard whitespace when running the program.
