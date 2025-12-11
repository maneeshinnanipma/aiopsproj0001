
import ast
from typing import Dict, Any

def parse_python_code(source: str) -> Dict[str, Any]:
    result = {"num_lines": len(source.splitlines()), "functions": [], "classes": [], "imports": []}
    try:
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                result["functions"].append(node.name)
            elif isinstance(node, ast.ClassDef):
                result["classes"].append(node.name)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    result["imports"].append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                result["imports"].append(node.module or "")
    except SyntaxError as e:
        result["error"] = f"SyntaxError: {e}"
    return result
