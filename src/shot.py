import asyncio
from loguru import logger

from mipac.client import Client
from env import HOST, TOKEN
from func import spam_action, text_helper

from type import TTarget

targets: list[TTarget] = [
    {'key': 'ctkpaarr', 'count': 0, 'dry_run': False},
    {'key': '荒らし.com', 'count': 0, 'dry_run': False},
    # { 'key': 'xn--68j5e377y.com', 'count': 0, 'dry_run': False },
    {'key': 'test', 'count': 0, 'dry_run': True},
]

"""
手動実行
"""


async def main():
    client = Client(f'https://{HOST}', TOKEN)
    await client.http.login()
    api = client.api
    me = await api.get_me()
    logger.success(f'Logged in: {me.username}')
    # 適宜IDは変えること
    note = await api.note.action.get('818dcf70d5d8fcec90f711a8')
    print(note.user.name, note.text)
    if note.user.host and len(note.mentions) >= 2:
        logger.info(f'スパムチェック開始: https://{HOST}/notes/{note.id}')

        for target in targets:
            if note.text is None:
                continue

            text = text_helper(note.text)
            if target['key'] in text:
                logger.success(f'パターン一致 {target['key']}')
                await spam_action(note, api, target)


if __name__ == '__main__':
    asyncio.run(main())
