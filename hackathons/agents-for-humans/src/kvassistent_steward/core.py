from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any


STOP_SMELL_MARKERS = ("rotting", "putrid", "acetone", "гнил", "ацетон")


@dataclass(frozen=True)
class SafetyDecision:
    status: str
    reason: str
    next_action: str


def safety_gate(
    *,
    mold_reported: bool = False,
    slime_reported: bool = False,
    smell_report: str = "unknown",
    liquid_temp_c: float | None = None,
) -> SafetyDecision:
    """Return a conservative decision using only observations the human supplied."""
    if mold_reported:
        return SafetyDecision(
            "stop",
            "The human reported mold.",
            "Stop the normal workflow. Do not taste the batch; discard it conservatively.",
        )
    if slime_reported:
        return SafetyDecision(
            "stop",
            "The human reported slime.",
            "Stop the normal workflow. Do not taste the batch; discard it conservatively.",
        )

    smell = (smell_report or "unknown").strip().lower()
    if smell != "unknown" and any(marker in smell for marker in STOP_SMELL_MARKERS):
        return SafetyDecision(
            "stop",
            "The human reported a smell associated with a failed batch.",
            "Stop the normal workflow. Do not taste the batch; discard it conservatively.",
        )

    if liquid_temp_c is not None and liquid_temp_c >= 35.0:
        return SafetyDecision(
            "stop_and_cool",
            f"Reported liquid temperature is {liquid_temp_c:.1f}°C.",
            "Stop the normal fermentation protocol, move the batch away from heat, and cool it before reassessing.",
        )

    return SafetyDecision(
        "continue",
        "No stop condition was reported in the supplied observations.",
        "Continue only from the observations already supplied; request any missing sensory check from the human.",
    )


def checkpoint_delay_hours(stage: str, liquid_temp_c: float | None) -> int:
    """Choose a conservative next check interval for the demo batch workflow."""
    normalized = stage.strip().lower()
    if normalized == "infusion":
        return 4
    if normalized == "primary_fermentation":
        if liquid_temp_c is not None and liquid_temp_c >= 28.0:
            return 4
        if liquid_temp_c is not None and liquid_temp_c >= 25.0:
            return 6
        return 8
    if normalized == "bottled":
        return 2
    if normalized == "chilled":
        return 12
    return 4


def next_checkpoint_iso(
    *,
    stage: str,
    liquid_temp_c: float | None,
    now: datetime | None = None,
) -> str:
    """Return the next UTC checkpoint as an ISO-8601 timestamp."""
    current = now or datetime.now(timezone.utc)
    if current.tzinfo is None:
        current = current.replace(tzinfo=timezone.utc)
    return (current + timedelta(hours=checkpoint_delay_hours(stage, liquid_temp_c))).astimezone(timezone.utc).isoformat()


def normalized_batch_state(
    *,
    batch_id: str,
    stage: str,
    liquid_temp_c: float | None,
    observation: str,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Create a small serializable state record without inventing missing facts."""
    current = now or datetime.now(timezone.utc)
    if current.tzinfo is None:
        current = current.replace(tzinfo=timezone.utc)
    return {
        "batch_id": batch_id,
        "stage": stage,
        "liquid_temp_c": liquid_temp_c,
        "observation": observation or "unknown",
        "updated_at": current.astimezone(timezone.utc).isoformat(),
        "next_checkpoint_at": next_checkpoint_iso(
            stage=stage,
            liquid_temp_c=liquid_temp_c,
            now=current,
        ),
    }
