interface props {
  text: string | null;
}

export default function ImmutableTextArea({ text }: props) {
  if (text == null) {
    text = "";
  }

  return (
    <div className="immutable-output">
      {text.split("\n").map((textLine) => (
        <>
          {textLine} <br />
        </>
      ))}
    </div>
  );
}
