"""Models for error response"""
from dataclasses import dataclass
from typing import Any


@dataclass
class ErrorResponse:
    """Response for api errors"""

    code: int
    name: str
    description: str
    message: str
    errors: list[Any]
