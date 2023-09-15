import asyncio
from typing import List

from clients.tg import TgClient
from clients.redis import RedisClient
from tools import app_data

from tools import Profile, ProfileDb

class Worker:
    def __init__(self, token: str, queue: asyncio.Queue, concurrent_workers: int):
        self.tg_client = TgClient(token)
        self.redis_client = RedisClient()
        self.queue = queue
        self.concurrent_workers = concurrent_workers
        self._tasks: List[asyncio.Task] = []

    async def handle_update(self, upd):
        if 'callback_query' in upd:
            message = upd['callback_query']['data']
            tg_id = upd['callback_query']['message']['chat']['id']
        else:
            message = upd['message']['text']
            tg_id = upd['message']['chat']['id']
        # creating profile
        tg_id_state = str(tg_id) + "_state"
        tg_id_data = str(tg_id) + "_data"
        r_client = self.redis_client.r
        if message == 'start':
            r_client.set(tg_id_state, 'creating_profile')
            r_client.delete(tg_id_data)
            r_client.hset(tg_id_data, mapping = {'initial': ''})
            await self.tg_client.send_message(tg_id, 'Give me your name')
        elif r_client.exists(tg_id_state) and r_client.get(tg_id_state) == 'creating_profile':
            for key, value in app_data.field_next_question.items():
                if key not in r_client.hgetall(tg_id_data):
                    r_client.hset(tg_id_data, key, message)
                    if key == 'goal':
                        r_client.hset(tg_id_data, 'tg_id', tg_id)
                        profile = Profile.Profile(r_client.hgetall(tg_id_data))
                        profile_db = ProfileDb.ProfileDb(profile)
                        profile_db.connect()
                        profile_db.save_to_db()
                        profile_db.disconnect()
                        r_client.delete(tg_id_data)
                        r_client.set(tg_id_state, 'nothing')
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