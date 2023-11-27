'''
Podload manager module.
'''

__all__ = (
    'Manager',
)

import logging

from .exceptions import PodcastNotFoundError
from .podcast import Podcast

LOGGER = logging.getLogger(__name__)


class Manager:
    '''
    The podcast manager.

    :param pathlib.Path podcasts_dir: The podcast directory
    '''

    def __init__(self, podcasts_dir):
        '''
        Constructor.
        '''
        self.podcasts_dir = podcasts_dir
        self.podcasts     = []

        self.load_podcasts()

    @property
    def info(self):
        '''
        The informations of all podcasts.

        :return: The informations
        :rtype: str
        '''
        info = []

        for podcast in self.podcasts:
            info.append(f'\n{podcast} ({podcast.metadata.get("retention")} days retention):')

            for title in podcast.info:
                info.append(f'    {title}')

        return '\n'.join(info)

    def load_podcasts(self):
        '''
        Load the podcasts from the disk.
        '''
        LOGGER.info('Loading podcasts from %s', self.podcasts_dir)

        if not self.podcasts_dir.exists():
            LOGGER.warning('Directory %s is missing, not loading podcasts', self.podcasts_dir)
            return

        for root, dirs, files in self.podcasts_dir.walk():  # pylint: disable=unused-variable
            for file in files:
                if file != Podcast.metadata_filename:
                    continue
                podcast = Podcast(root)
                LOGGER.info('Found %r podcast at %r', str(podcast), str(root))
                self.podcasts.append(podcast)

    def add_podcast(self, **kwargs):
        '''
        Add a new podcast.

        :param dict \\**kwargs: The kwargs to pass to :meth:`podload.podcast.Podcast.create()`
        '''
        self.podcasts.append(Podcast.create(podcasts_dir=self.podcasts_dir, **kwargs))

    def delegate(self, method, **kwargs):
        '''
        Delegate a method to all podcasts.

        :param str method: The name of the method :class:`podload.podcast.Podcast`
        :param dict \\**kwargs: The kwargs to pass to :meth:`podload.podcast.Podcast.download()`
        '''
        for podcast in self.podcasts:
            getattr(podcast, method)(**kwargs)

    def set_retention(self, podcast, retention):
        '''
        Set a new retention on a podcast.

        :param str podcast: The podcast title
        :param int retention: The retention in days

        :raises podload.exceptions.PodcastNotFoundError: When podcast wasn't found
        '''
        for podcast_obj in self.podcasts:
            if podcast_obj.metadata['title'] == podcast:
                podcast_obj.set_retention(retention)
                return

        error = 'Podcast "%s" not found'
        LOGGER.error(error, podcast)
        raise PodcastNotFoundError(error % podcast)

    def clean(self, **kwargs):
        '''
        Download all episodes.

        :param dict \\**kwargs: The kwargs to pass to :meth:`podload.podcast.Podcast.download()`
        '''
        self.delegate('clean', **kwargs)

    def download(self, **kwargs):
        '''
        Download all episodes.

        :param dict \\**kwargs: The kwargs to pass to :meth:`podload.podcast.Podcast.download()`
        '''
        self.delegate('download', **kwargs)
