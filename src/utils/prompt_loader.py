from pathlib import Path

# Determine the src folder dynamically (this file is inside src/utils)
SRC_ROOT = Path(__file__).resolve().parent.parent


def load_prompt(filename: str) -> str:
    """
    Load a prompt text file from the src/prompts folder.

    Args:
        filename (str): Name of the prompt file (e.g., "planner_instruction.txt")

    Returns:
        str: Contents of the prompt file.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    file_path = SRC_ROOT / "prompts" / filename
    if not file_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {file_path}")
    return file_path.read_text(encoding="utf-8")
