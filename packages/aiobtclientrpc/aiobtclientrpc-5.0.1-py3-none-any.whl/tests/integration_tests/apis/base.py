class APIBase:
    def log(self, *args):
        print(f'{self.client.label} API:', ' '.join(str(arg) for arg in args))

    async def reset(self):
        # Delete all torrents
        infohashes = await self.get_torrent_list()
        if infohashes:
            self.log('Resetting: Deleting torrents:', infohashes)
            await self.remove_torrents(infohashes)
            infohashes = await self.get_torrent_list()
            assert infohashes == [], infohashes
