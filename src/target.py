# SPDX-FileCopyrightText: sousuke0422 and All Contributor
# SPDX-License-Identifier: MIT

from src.type import TTarget

TARGETS: list[TTarget] = [
    # 照査パターン
    {'key': 'ctkpaarr', 'count': 0, 'dry_run': False},
    {'key': '荒らし.com', 'count': 0, 'dry_run': False},
    {'key': '画像が貼れなかったのでメンションだけします', 'count': 0, 'dry_run': False},
    # { 'key': 'xn--68j5e377y.com', 'count': 0, 'dry_run': False },
    {'key': '#鈴木哲哉', 'count': 0, 'dry_run': False},
    {'key': 'yip.su/25X8U6', 'count': 0, 'dry_run': False},

    # テスト用
    {'key': 'test', 'count': 0, 'dry_run': True},
]
