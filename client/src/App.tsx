import { useState, useRef } from "react";
import { io } from "socket.io-client";
import "./App.css";

function App() {
  // const LOCAL_HOST = "http://127.0.0.1:3002";
  const [currentOutput, setCurrentOutput] = useState<string | null>(null);

  let codeRef: React.MutableRefObject<any> = useRef<string>(null);
  let outputRef: React.MutableRefObject<any> = useRef<string>(null);

  const socket = io("http://127.0.0.1:3002/", {
    withCredentials: true,
  });
  socket.on("connect", () => {
    console.log("socket connected with server");
  });

  socket.on("input-event", (message) => {
    console.log("input statement detected. message from server: ");
    console.log(message);
    return;
    // socket.emit("input-provided", "420");
  });

  async function getOutput(e: any) {
    e.preventDefault();
    outputRef.current.focus();

    // socket.on("input-event", (message) => {
    //   console.log("input statement detected. message from server: ");
    //   console.log(message);
    //   socket.emit("input-provided", "420");
    // });
    if (codeRef.current) {
      const inputCode = codeRef.current.value;
      const rawBody = JSON.stringify({
        body: inputCode,
      });

      socket.emit("run-interpreter", rawBody);

      // const response = await fetch(`${LOCAL_HOST}/interpreter`, {
      //   method: "POST",
      //   headers: {
      //     "Content-Type": "application/json",
      //     "Access-Control-Allow-Origin": "*",
      //   },

      //   body: rawBody,
      // });
      // const data = await response.text();
      socket.once("user-input", (terminalOutput: string, numInputs: number) => {
        console.log(terminalOutput);
        console.log(numInputs);
        outputRef.current.focus();
      });
      // if (data[data.length - 1] == "@") {

      // }
      // console.log(data);
      // setCurrentOutput(data);
    }
  }

  return (
    <>
      <h1> BASIC Interpreter </h1>
      <button onClick={getOutput}> Run </button>
      <div className="base">
        <div className="editor">
          <textarea className="code-input" ref={codeRef}></textarea>
        </div>

        <div className="output">
          <textarea
            className="code-input code-output"
            onChange={(e) => setCurrentOutput(e.target.value)}
            ref={outputRef}
            value={currentOutput ? currentOutput : ""}
          />
        </div>
      </div>
    </>
  );
}

export default App;
