from collections.abc import Iterable
from pathlib import Path
from typing import Any

import srsly  # type: ignore


def create_pattern_file(
    id: str,
    patterns: Iterable[list[dict[str, Any]]],
    folder: Path | None = None,
    label: str | None = None,
):
    fname = f"{id}.jsonl"
    data = [{"id": id, "label": label or id.upper(), "pattern": p} for p in patterns]
    target = folder.joinpath(fname) if folder and folder.exists() else fname
    srsly.write_jsonl(path=target, lines=data)
