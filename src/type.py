# SPDX-FileCopyrightText: sousuke0422 and All Contributor
# SPDX-License-Identifier: MIT

from typing import TypedDict

class TTarget(TypedDict):
    key: str
    count: int
    dry_run: bool
