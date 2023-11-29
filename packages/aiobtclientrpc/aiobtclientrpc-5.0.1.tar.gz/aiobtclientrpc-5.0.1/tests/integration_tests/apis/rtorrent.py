from . import base


class API(base.APIBase):
    def __init__(self, client):
        self.client = client

    async def perform_simple_request(self):
        result = await self.client.call('system.listMethods')
        self.log('system.listMethods:', result)
        assert 'system.listMethods' in result
        assert 'system.multicall' in result
        assert 'load.normal' in result

        result = await self.client.call('dht.statistics')
        self.log('dht.statistics:', result)
        assert result['dht'] == 'off'

        result = await self.client.call('protocol.pex')
        self.log('protocol.pex:', result)
        assert result == 0

    async def get_torrent_list(self):
        result = await self.client.call('download_list', '')
        self.log('download_list:', result)
        infohashes = sorted(infohash.lower() for infohash in result)
        return infohashes

    STATE_PAUSED = 0
    STATE_STARTED = 1

    async def add_torrents(self, torrent_filepaths, download_path='/tmp/some/path', paused=False):
        # Add torrents
        calls = []
        method_name = 'load.raw' if paused else 'load.raw_start'
        for filepath in torrent_filepaths:
            calls.append({
                'methodName': method_name,
                'params': [
                    '',
                    open(filepath, 'rb').read(),
                    # Set download location
                    f'd.directory_base.set="{download_path}"',
                    # Untie torrent from .torrent file so rtorrent doesn't
                    # delete it when the torrent is removed.
                    'd.tied_to_file.set='
                ],
            })
        result = await self.client.call('system.multicall', calls)
        self.log('load:', result)

        # Get added torrent hashes from server
        infohashes = await self.client.call('download_list', '')
        infohashes = [infohash.lower() for infohash in infohashes]

        # Verify torrents where correctly added
        fields = ('hash', 'state', 'directory_base')
        multicall_params = (
            ['main']
            + [f'd.{field}=' for field in fields]
        )
        result = await self.client.call('d.multicall2', '', multicall_params)
        torrents = [{field: value for field, value in zip(fields, item)}
                    for item in result]
        self.log('torrents:', torrents)
        for torrent in torrents:
            location = torrent['directory_base']
            state = torrent['state']
            assert location == download_path, f'{location!r} != {download_path!r}'
            if paused:
                assert state == self.STATE_PAUSED, f'{state!r} != {self.STATE_PAUSED!r}'
            else:
                assert state == self.STATE_STARTED, f'{state!r} != {self.STATE_STARTED!r}'

        added_infohashes = sorted(torrent['hash'].lower() for torrent in torrents)
        self.log('added torrents:', added_infohashes)
        return added_infohashes

    async def remove_torrents(self, infohashes):
        for infohash in infohashes:
            result = await self.client.call('d.erase', infohash)
            self.log(f'd.erase {infohash}:', result)

    async def on_torrent_added(self, handler):
        # Raise NotImplementedError
        await self.client.add_event_handler('<event name>', handler)

    async def wait_for_torrent_added(self):
        # Raise NotImplementedError
        await self.client.wait_for_event('<event name>')
