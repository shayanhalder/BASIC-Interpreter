import { useState, useRef } from "react";
import { io } from "socket.io-client";
import ImmutableTextArea from "./ImmutableTextArea";
import "./App.css";

function App() {
  const LOCAL_HOST = "http://127.0.0.1:3002";
  const [userInput, setUserInput] = useState<string | null>(null);
  const [currentOutput, setCurrentOutput] = useState<string | null>(null);

  let codeRef: React.MutableRefObject<any> = useRef<string>(null);
  let outputRef: React.MutableRefObject<any> = useRef<string>(null);
  let rightRef: React.MutableRefObject<any> = useRef<string>(null);

  const socket = io(LOCAL_HOST, {
    withCredentials: true,
  });

  socket.on("connect", () => {
    console.log("Client established socket connection with server");
  });

  socket.on("execution-finished", (interpreterState) => {
    console.log("Execution-Finished event received from server");
    console.log("Interpreter State: ");
    console.log(interpreterState);
    setCurrentOutput(interpreterState["output"]);
  });

  socket.on("input-event", (interpreterState) => {
    console.log("Input-Event event response received from server");
    console.log("Interpreter State: ");
    console.log(interpreterState);

    const lastLine = interpreterState["current_line"];
    const inputCode = interpreterState["lines"].split("\n");

    const userInput = prompt(`${inputCode[lastLine]}`);

    interpreterState["user_input"] = userInput;
    const newRawBody = JSON.stringify({
      body: interpreterState,
    });

    socket.emit("continue-execution", newRawBody);
  });

  async function getOutput(e: any) {
    outputRef.current.focus();

    if (codeRef.current) {
      const inputCode = codeRef.current.value;
      const rawBody = JSON.stringify({
        body: inputCode,
      });
      socket.emit("run-interpreter", rawBody);
    }
  }

  return (
    <>
      <h1> BASIC Interpreter </h1>
      <button onClick={(e) => getOutput(e)}> Run </button>
      <div className="base">
        <div className="editor">
          <textarea className="code-input" ref={codeRef}></textarea>
        </div>

        <div
          className="output"
          ref={rightRef}
          onFocus={() => (rightRef.current.style.border = "2px solid #99C8FF")}
          onBlur={() => (rightRef.current.style.border = "1px solid white")}
        >
          <ImmutableTextArea text={currentOutput} />

          <textarea
            className="code-input code-output"
            onChange={(e) => setUserInput(e.target.value)}
            ref={outputRef}
            value={userInput ? userInput : ""}
          />
        </div>
      </div>
    </>
  );
}

export default App;
