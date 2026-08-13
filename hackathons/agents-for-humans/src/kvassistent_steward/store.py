from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


DEFAULT_STATE_PATH = Path(".kvassistent-steward-state.json")


def state_path() -> Path:
    return Path(os.environ.get("KVASSISTENT_STATE_PATH", DEFAULT_STATE_PATH))


def _load_all(path: Path | None = None) -> dict[str, dict[str, Any]]:
    target = path or state_path()
    if not target.exists():
        return {}
    data = json.loads(target.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("State file must contain a JSON object")
    return data


def load_batch(batch_id: str, path: Path | None = None) -> dict[str, Any] | None:
    return _load_all(path).get(batch_id)


def save_batch(batch: dict[str, Any], path: Path | None = None) -> dict[str, Any]:
    target = path or state_path()
    all_batches = _load_all(target)
    batch_id = str(batch["batch_id"])
    all_batches[batch_id] = batch
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(target.suffix + ".tmp")
    temporary.write_text(
        json.dumps(all_batches, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(target)
    return batch
