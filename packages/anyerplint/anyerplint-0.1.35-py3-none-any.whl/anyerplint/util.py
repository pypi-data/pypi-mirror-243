from pathlib import Path
from typing import IO

import chardet


def open_text_file(file_path: str | Path) -> IO[str]:
    enc = guess_encoding(file_path)
    f = open(file_path, encoding=enc)
    return f


def guess_encoding(file_path: str | Path, byte_count: int = 1024) -> str | None:
    with open(file_path, "rb") as file:
        data = file.read(byte_count)

    result = chardet.detect(data)
    encoding = result["encoding"]
    return "utf-8" if encoding == "ascii" else encoding
