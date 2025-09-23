from flask import Flask, request, jsonify
from flask_cors import CORS
import ast

app = Flask(__name__)
CORS(app, origins=["https://keemzzzone.github.io"])

SAFE_BUILTINS = {
    "print": print,
    "len": len,
    "range": range,
    "int": int,
    "str": str,
    "float": float,
    "bool": bool,
    "list": list,
    "dict": dict,
    "set": set,
    "tuple": tuple,
    "sum": sum,
    "min": min,
    "max": max,
    "abs": abs
}

def is_safe(code: str) -> bool:
    try:
        tree = ast.parse(code)
    except Exception:
        return False
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            return False
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id in ["exec", "eval", "open", "__import__", "compile"]:
                    return False
    return True

@app.route("/run", methods=["POST"])
def run_code():
    data = request.get_json()
    code = data.get("code", "")

    if not is_safe(code):
        return jsonify({"error": "안전하지 않은 코드가 감지되었습니다."}), 400

    try:
        output = []

        def safe_print(*args, **kwargs):
            output.append(" ".join(map(str, args)))

        safe_globals = {"__builtins__": {**SAFE_BUILTINS, "print": safe_print}}
        safe_locals = {}

        exec(code, safe_globals, safe_locals)

        return jsonify({"output": "\n".join(output) if output else "실행 완료 (출력 없음)"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
