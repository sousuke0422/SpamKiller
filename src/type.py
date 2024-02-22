from typing import TypedDict

TTarget = TypedDict('TTarget', {
    'key': str,
    'count': int,
    'dry_run': bool
})
