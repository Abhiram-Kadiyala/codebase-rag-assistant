import ast


def extract_python_chunks(file_path: str, content: str):
    chunks = []

    try:
        tree = ast.parse(content)
    except SyntaxError:
        return chunks

    lines = content.splitlines()

    def get_code(node):
        start_line = node.lineno
        end_line = getattr(node, "end_lineno", start_line)

        code = "\n".join(
            lines[start_line - 1:end_line]
        )

        return start_line, end_line, code

    # Look at top-level items
    for node in tree.body:

        # Top-level function
        if isinstance(
            node,
            (ast.FunctionDef, ast.AsyncFunctionDef)
        ):
            start_line, end_line, code = get_code(node)

            chunks.append({
                "file": file_path,
                "type": "function",
                "name": node.name,
                "qualified_name": node.name,
                "start_line": start_line,
                "end_line": end_line,
                "code": code
            })

        # Class
        elif isinstance(node, ast.ClassDef):

            class_name = node.name

            # Extract methods individually
            for item in node.body:

                if isinstance(
                    item,
                    (ast.FunctionDef, ast.AsyncFunctionDef)
                ):
                    start_line, end_line, code = get_code(item)

                    chunks.append({
                        "file": file_path,
                        "type": "method",
                        "name": item.name,
                        "qualified_name": f"{class_name}.{item.name}",
                        "class_name": class_name,
                        "start_line": start_line,
                        "end_line": end_line,
                        "code": code
                    })

    return chunks


def extract_generic_chunks(file_path: str, content: str):
    chunks = []

    lines = content.splitlines()

    chunk_size = 60
    overlap = 10

    start = 0
    chunk_number = 1

    while start < len(lines):

        end = min(
            start + chunk_size,
            len(lines)
        )

        code = "\n".join(
            lines[start:end]
        )

        if code.strip():

            chunks.append({
                "file": file_path,
                "type": "code",
                "name": f"chunk_{chunk_number}",
                "qualified_name": f"{file_path}:chunk_{chunk_number}",
                "start_line": start + 1,
                "end_line": end,
                "code": code
            })

        chunk_number += 1

        if end == len(lines):
            break

        start = end - overlap

    return chunks