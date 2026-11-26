import ast

def analyze_structure(source_code: str) -> dict:
    """Identify Python constructs without executing the code."""

    try:
        tree = ast.parse(source_code)
    except SyntaxError:
        return {
            "valid": False,
            "if_branches": None,
            "for_loops": None,
            "while_loops": None,
            "functions": None,
        }

    nodes = list(ast.walk(tree))

    return {
        "valid": True,
        "if_branches": sum(
            isinstance(node, ast.If) for node in nodes
        ),
        "for_loops": sum(
            isinstance(node, ast.For) for node in nodes
        ),
        "while_loops": sum(
            isinstance(node, ast.While) for node in nodes
        ),
        "functions": sum(
            isinstance(node, ast.FunctionDef) for node in nodes
        ),
    }
