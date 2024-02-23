import asyncio
from aiohttp import ClientWebSocketResponse

from loguru import logger

from mipa import Note
from mipa.ext.commands.bot import Bot
from env import HOST, TOKEN

from func import spam_action, text_helper
from type import TTarget



targets: list[TTarget] = [
        { 'key': 'ctkpaarr', 'count': 0, 'dry_run': False },
        { 'key': '荒らし.com', 'count': 0, 'dry_run': False },
        # { 'key': 'xn--68j5e377y.com', 'count': 0, 'dry_run': False },
        { 'key': 'test', 'count': 0, 'dry_run': True}
    ]

class SpamKiller(Bot):
    def __init__(self):
        super().__init__()

    async def _connect_channel(self):
        await self.router.connect_channel(['main', 'global'])

    async def on_ready(self, ws: ClientWebSocketResponse):
        await self._connect_channel()
        logger.success(f'Logged in: {self.user.username}')

    async def on_reconnect(self, ws: ClientWebSocketResponse):
        await self._connect_channel()

    async def on_note(self, note: Note):
        if note.user.host and len(note.mentions) >= 2:
            logger.info(f'スパムチェック開始: https://{HOST}/notes/{note.id}')
            # print(len(note.mentions))
            # print(note.user.username, note.text)
            for target in targets:
                text = text_helper(note.text)
                if target['key'] in text:
                    logger.success(f'パターン一致 {target['key']}')
                    await spam_action(note, self.client, target)
                    continue

            #if note.file_ids is not 0:
            #    logger.error('画像チェック機能は未実装')

if __name__ == '__main__':
    bot = SpamKiller()
    asyncio.run(bot.start(f'wss://{HOST}/streaming', TOKEN))
