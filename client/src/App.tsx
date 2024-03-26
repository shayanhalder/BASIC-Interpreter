import { useState, useRef } from "react";
import { io } from "socket.io-client";
import ImmutableTextArea from "./ImmutableTextArea";
import "./App.css";

function App() {
  // const LOCAL_HOST = "http://127.0.0.1:3002";
  const [userInput, setUserInput] = useState<string | null>(null);
  const [currentOutput, setCurrentOutput] = useState<string | null>("POTATO\nTOMATO\n3\n5");

  let codeRef: React.MutableRefObject<any> = useRef<string>(null);
  let outputRef: React.MutableRefObject<any> = useRef<string>(null);
  let rightRef: React.MutableRefObject<any> = useRef<string>(null);

  // const socket = io("http://127.0.0.1:3002/", {
  //   withCredentials: true,
  // });
  // socket.on("connect", () => {
  //   console.log("socket connected with server");
  // });

  // socket.on("input-event", (message) => {
  //   console.log("input statement detected. message from server: ");
  //   console.log(message);
  //   return;
  //   // socket.emit("input-provided", "420");
  // });

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

      // socket.emit("run-interpreter", rawBody);

      // const response = await fetch(`${LOCAL_HOST}/interpreter`, {
      //   method: "POST",
      //   headers: {
      //     "Content-Type": "application/json",
      //     "Access-Control-Allow-Origin": "*",
      //   },

      //   body: rawBody,
      // });
      // const data = await response.text();
      // socket.once("user-input", (terminalOutput: string, numInputs: number) => {
      //   console.log(terminalOutput);
      //   console.log(numInputs);
      //   outputRef.current.focus();
      // });
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
