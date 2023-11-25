"""Module providing data class to represent registered event models."""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class CloudEventDoc(BaseModel):
    """Document describing what data models are published where."""

    api_version: str
    data_models: dict[str, dict[str, Any]] = {}
