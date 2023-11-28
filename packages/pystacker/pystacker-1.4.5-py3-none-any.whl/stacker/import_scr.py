from pathlib import Path
from stacker.stacker import Stacker


def import_stacker_script(filename: str | Path):
    """Import a stacker script and return the stacker object."""

    if isinstance(filename, str):
        filename = Path(filename).resolve()
    if not filename.is_file():
        raise FileNotFoundError(f"File {filename} not found.")
    if not filename.exists():
        raise FileNotFoundError(f"File {filename} not found.")
    if filename.suffix != ".stk":
        raise ValueError(f"File {filename} is not a stacker script.")

    with open(filename, 'r') as file:
        script_content = file.read()


    return script_content


if __name__ == "__main__":
    s = import_stacker_script("test.stk")
    print(s)