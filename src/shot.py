"""
手動実行
"""

import asyncio

from loguru import logger
from mipac.client import Client

from env import HOST, TOKEN
from func import spam_action, text_helper
from target import TARGETS


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

        for target in TARGETS:
            if note.text is None:
                continue

            text = text_helper(note.text)
            if target['key'] in text:
                logger.success(f'パターン一致 {target['key']}')
                await spam_action(note, api, target)


if __name__ == '__main__':
    asyncio.run(main())
