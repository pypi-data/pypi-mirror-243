import os

from .. import common
from . import base


class API(base.APIBase):
    def __init__(self, client):
        self.client = client

    async def perform_simple_request(self):
        result = await self.client.call('core.get_config')
        self.log('daemon.get_config:', result)
        assert result['dht'] is False
        assert result['utpex'] is False

    async def get_torrent_list(self):
        result = await self.client.call('core.get_torrents_status', filter_dict={}, keys=['name'])
        self.log('core.get_torrents_status:', result)
        infohashes = sorted(result.keys())
        return infohashes

    async def add_torrents(self, torrent_filepaths, download_path='/tmp/some/path', paused=True):
        # Register event handler for added torrents
        torrents_added = []

        def on_torrent_added(infohash, from_state_):
            self.log('torrent added:', infohash, from_state_)
            torrents_added.append(infohash)

        await self.client.add_event_handler('TorrentAddedEvent', on_torrent_added)

        # Add torrents (as_file is ignored because Deluge doesn't accept file
        # paths)
        for filepath in torrent_filepaths:
            result = await self.client.call(
                'core.add_torrent_file',
                filename=os.path.basename(filepath),
                filedump=common.read_torrent_file(filepath),
                options={
                    'add_paused': paused,
                    'save_path': download_path,
                },
            )
            self.log('core.add_torrent_file_async', result)

        assert torrents_added

        # Verify torrents were correctly added
        result = await self.client.call(
            'core.get_torrents_status',
            filter_dict={'id': torrents_added},
            keys=['paused', 'save_path'],
        )
        self.log('core.get_torrents_status:', torrents_added, result)
        for infohash, torrent in result.items():
            assert torrent['save_path'] == download_path, torrent['save_path']
            if paused:
                assert torrent['paused'] is True, repr(torrent['paused'])
            else:
                assert torrent['paused'] is False, repr(torrent['paused'])

        return sorted(torrents_added)

    async def remove_torrents(self, infohashes):
        # Register event handler
        torrents_removed = []

        def on_torrent_removed(infohash):
            self.log('torrent removed:', infohash)
            torrents_removed.append(infohash)

        await self.client.add_event_handler('TorrentRemovedEvent', on_torrent_removed)

        # Remove torrents
        for infohash in infohashes:
            result = await self.client.call(
                'core.remove_torrent',
                torrent_id=infohash,
                remove_data=False,
            )
            self.log(f'core.remove_torrent {infohash}', result)

        # Check if events occured as expected
        assert torrents_removed == infohashes

    async def on_torrent_added(self, handler):
        def handler_wrapper(infohash, *args, **kwargs):
            handler(infohash)
        await self.client.add_event_handler('TorrentAddedEvent', handler_wrapper)

    async def wait_for_torrent_added(self):
        await self.client.wait_for_event('TorrentAddedEvent')
