from typing import TypedDict


class TTarget(TypedDict):
    key: str
    count: int
    dry_run: bool
