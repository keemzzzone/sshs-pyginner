require.config({
  paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.44.0/min/vs' }
});

let editor;

require(["vs/editor/editor.main"], function () {
  editor = monaco.editor.create(document.getElementById("editor"), {
    value: "print('Hello from GitHub Pages!')",
    language: "python",
    theme: "vs-dark",
    automaticLayout: true
  });
});

function runCode() {
  const code = editor.getValue();

  fetch("hhttps://keemzzzone.pythonanywhere.com/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code: code })
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById("output").textContent = data.output || ("Error: " + data.error);
  })
  .catch(err => {
    document.getElementById("output").textContent = "Request failed: " + err;
  });
}
