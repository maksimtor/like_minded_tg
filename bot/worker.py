import asyncio
from typing import List

from clients.tg import TgClient
from tools import app_data

from tools import Profile, ProfileDb

class Worker:
    def __init__(self, token: str, queue: asyncio.Queue, concurrent_workers: int):
        self.tg_client = TgClient(token)
        self.queue = queue
        self.concurrent_workers = concurrent_workers
        self._tasks: List[asyncio.Task] = []
        self.state = {}

    async def handle_update(self, upd):
        if 'callback_query' in upd:
            message = upd['callback_query']['data']
            tg_id = upd['callback_query']['message']['chat']['id']
        else:
            message = upd['message']['text']
            tg_id = upd['message']['chat']['id']
        # creating profile
        if message == 'start':
            self.state[tg_id] = {'state': 'creating_profile', 'data': {}}
            await self.tg_client.send_message(tg_id, 'Give me your name')
        elif self.state.get(tg_id, None) and self.state[tg_id]['state'] == 'creating_profile':
            for key, value in app_data.field_next_question.items():
                if key not in self.state[tg_id]['data']:
                    if key in ['interests', 'music']:
                        message = list(message.split(','))
                    elif key in ['pol_coords', 'geo_coords', 'personality', 'age_pref']:
                        message = tuple(map(float, message.split(',')))
                    self.state[tg_id]['data'][key] = message
                    if key == 'goal':
                        self.state[tg_id]['data']['tg_id'] = tg_id
                        profile = Profile.Profile(self.state[tg_id]['data'])
                        profile_db = ProfileDb.ProfileDb(profile)
                        profile_db.connect()
                        profile_db.save_to_db()
                        profile_db.disconnect()
                        self.state[tg_id] = {}
                        await self.tg_client.send_message(tg_id, "Done")
                    else: await self.tg_client.send_message(tg_id, value)
                    break
        elif message == 'search':
            profile_db = ProfileDb.ProfileDb()
            profile_db.connect()
            profiles = profile_db.potential_matches(tg_id)
            profile_db.disconnect()
            await self.tg_client.send_message(tg_id, str(profiles[0].public_data()))

    async def _worker(self):
        while True:
            upd = await self.queue.get()
            try:
                await self.handle_update(upd)
            except Exception as e:
                print(e)
            finally:
                self.queue.task_done()

    async def start(self):
        self._tasks = [asyncio.create_task(self._worker()) for _ in range(self.concurrent_workers)]

    async def stop(self):
        await self.queue.join()
        for t in self._tasks:
            t.cancel()