import os
import shutil
import tempfile

from git import Repo


SUPPORTED_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java",
    ".cpp",
    ".c",
    ".h",
    ".cs",
    ".go",
    ".php",
    ".rb"
}


IGNORED_DIRECTORIES = {
    ".git",
    "node_modules",
    "venv",
    ".venv",
    "__pycache__",
    "dist",
    "build",
    ".next"
}


def clone_repository(repo_url: str):
    temp_dir = tempfile.mkdtemp()

    try:
        Repo.clone_from(
            repo_url,
            temp_dir,
            depth=1,
            single_branch=True
        )

        return temp_dir

    except Exception as e:
        shutil.rmtree(
            temp_dir,
            ignore_errors=True
        )

        raise Exception(
            f"Failed to clone repository: {str(e)}"
        )


def read_code_files(repo_path: str):

    files = []

    for root, dirs, filenames in os.walk(repo_path):

        # Ignore folders that contain generated files,
        # dependencies, caches, or Git metadata.
        dirs[:] = [
            directory
            for directory in dirs
            if directory not in IGNORED_DIRECTORIES
        ]

        for filename in filenames:

            extension = os.path.splitext(
                filename
            )[1].lower()

            if extension not in SUPPORTED_EXTENSIONS:
                continue

            full_path = os.path.join(
                root,
                filename
            )

            relative_path = os.path.relpath(
                full_path,
                repo_path
            )

            try:
                with open(
                    full_path,
                    "r",
                    encoding="utf-8",
                    errors="ignore"
                ) as file:

                    content = file.read()

                # Skip empty files
                if not content.strip():
                    continue

                files.append({
                    "path": relative_path.replace(
                        "\\",
                        "/"
                    ),
                    "extension": extension,
                    "content": content
                })

            except Exception:
                # If a file cannot be read,
                # skip it instead of crashing the scan.
                continue

    return files