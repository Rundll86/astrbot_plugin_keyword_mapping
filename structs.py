from pathlib import Path
from typing import Any

from pydantic import BaseModel


class GroupState(BaseModel):
    switch: bool
    ban_keywords: list[str]

    def __init__(self) -> None:
        super().__init__(switch=True, ban_keywords=[])

    def format(self) -> str:
        return f"关键词映射：{'开' if self.switch else '关'}，关键词剔除列表：{'，'.join(self.ban_keywords)}"

    def write(self, fp: str | Path):
        with SafeFileStream(fp, None, True) as file:
            file.write(self.model_dump_json())

    @classmethod
    def read(cls, fp: str | Path):
        with SafeFileStream(
            fp,
            {
                "switch": True,
                "ban_keywords": [],
            },
        ) as file:
            return cls.model_validate_json(file.read())


class SafeFileStream:
    def __init__(
        self,
        fp: str | Path,
        default: Any,
        write: bool = False,
        binary: bool = False,
    ) -> None:
        self.default = default
        self.file_path = fp
        self.write_mode = write
        self.binary_mode = binary
        self.stream = None

    def __enter__(self):
        try:
            self.stream = open(
                self.file_path,
                f"{'w+' if self.write_mode else 'r'}{'b' if self.binary_mode else ''}",
                encoding=None if self.binary_mode else "utf8",
            )
        except Exception:
            self.stream = None
        return self

    def __exit__(self, exc_type, exc, tb):
        if self.stream is not None:
            self.stream.close()

    def read(self):
        if self.stream is None:
            return self.default
        else:
            return self.stream.read()

    def write(self, data: Any):
        if self.stream is None:
            self.default = data
        else:
            self.stream.write(data)
