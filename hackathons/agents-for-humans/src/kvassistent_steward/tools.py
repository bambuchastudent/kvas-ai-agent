from __future__ import annotations

import json
from datetime import datetime, timezone

from strands import tool

from .core import normalized_batch_state, safety_gate
from .store import load_batch as load_batch_record
from .store import save_batch


@tool
def get_batch_state(batch_id: str) -> str:
    """Load the last persisted state for a fermentation batch.

    Args:
        batch_id: Stable identifier chosen for the human's batch.
    """
    batch = load_batch_record(batch_id)
    if batch is None:
        return json.dumps({"found": False, "batch_id": batch_id})
    return json.dumps({"found": True, "batch": batch}, ensure_ascii=False)


@tool
def record_batch_state(
    batch_id: str,
    stage: str,
    observation: str = "unknown",
    liquid_temp_c: float | None = None,
) -> str:
    """Persist only fermentation state explicitly supplied by the human.

    Args:
        batch_id: Stable identifier for the batch.
        stage: Current workflow stage, for example infusion or primary_fermentation.
        observation: Human-supplied observation. Use unknown when it was not reported.
        liquid_temp_c: Human-measured liquid temperature in Celsius, if available.
    """
    batch = normalized_batch_state(
        batch_id=batch_id,
        stage=stage,
        liquid_temp_c=liquid_temp_c,
        observation=observation,
    )
    save_batch(batch)
    return json.dumps(batch, ensure_ascii=False)


@tool
def assess_reported_safety(
    mold_reported: bool = False,
    slime_reported: bool = False,
    smell_report: str = "unknown",
    liquid_temp_c: float | None = None,
) -> str:
    """Apply conservative safety gates to observations the human actually reported.

    Args:
        mold_reported: True only when the human explicitly reports visible mold.
        slime_reported: True only when the human explicitly reports slime.
        smell_report: Human-reported smell, or unknown when no smell was reported.
        liquid_temp_c: Human-measured liquid temperature in Celsius, if available.
    """
    decision = safety_gate(
        mold_reported=mold_reported,
        slime_reported=slime_reported,
        smell_report=smell_report,
        liquid_temp_c=liquid_temp_c,
    )
    return json.dumps(
        {
            "status": decision.status,
            "reason": decision.reason,
            "next_action": decision.next_action,
        },
        ensure_ascii=False,
    )


@tool
def due_checkpoint(batch_id: str) -> str:
    """Check whether the persisted batch currently needs a human checkpoint.

    Args:
        batch_id: Stable identifier for the batch.
    """
    batch = load_batch_record(batch_id)
    if batch is None:
        return json.dumps({"found": False, "batch_id": batch_id})

    checkpoint_raw = batch.get("next_checkpoint_at")
    if not checkpoint_raw:
        return json.dumps({"found": True, "due": True, "reason": "checkpoint_missing"})

    checkpoint = datetime.fromisoformat(str(checkpoint_raw).replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)
    due = checkpoint <= now
    return json.dumps(
        {
            "found": True,
            "due": due,
            "next_checkpoint_at": checkpoint.astimezone(timezone.utc).isoformat(),
            "stage": batch.get("stage"),
            "observation": batch.get("observation", "unknown"),
        },
        ensure_ascii=False,
    )
