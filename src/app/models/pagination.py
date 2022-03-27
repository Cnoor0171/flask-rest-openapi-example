"""Pagination models"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Pagination:
    """Response pagination info"""

    current: int
    page_size: int
    next: Optional[int]
    prev: Optional[int]
    page_count: int
