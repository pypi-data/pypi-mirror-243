'''
Podload podcast module.
'''

__all__ = (
    'Podcast',
)

import datetime
import email.utils
import json
import logging
import os
import pathlib
import re
import urllib.parse
import urllib.request

import feedparser
import pytz

from . import exceptions

#: The logger instance.
LOGGER   = logging.getLogger(__name__)

#: The local timezone to use.
TIMEZONE = pytz.timezone('Europe/Zurich')

#: The default retention in days.
DEFAULT_RETENTION = 7


class Podcast:
    '''
    A single podcast.

    :param pathlib.Path podcast_dir: The podcast directory
    '''

    #: The name of the metadata file.
    metadata_filename = '.podload'

    #: Accepted link mime types.
    accepted_types = (
        'audio/mpeg',
    )

    @classmethod
    def parse_feed_url(cls, url):
        '''
        Parse a feed URL, verify its payload and return the feed.

        :param str url: The feed URL

        :return: The feed
        :rtype: feedparser.util.FeedParserDict

        :raises podload.exceptions.FeedError: When there was a feed error
        '''
        LOGGER.debug('Parsing podcast at %r', url)

        feed = feedparser.parse(url)

        try:
            assert feed, 'feed'
            assert hasattr(feed, 'feed') and feed.feed, 'feed informations'
            assert hasattr(feed.feed, 'title') and feed.feed.title, 'feed title'
            assert feed.entries, 'feed entries'
        except AssertionError as ex:
            error = 'Could not retreive %s from podcast at %r'
            LOGGER.error(error, ex, url)
            raise exceptions.FeedError(error % (ex, url)) from ex

        return feed

    @classmethod
    def create(cls, podcasts_dir, url, retention=DEFAULT_RETENTION):
        '''
        Create a new podcast from an URL.

        This will create a new directory with the meta file in it.

        :param pathlib.Path podcasts_dir: The podcasts directory
        :param str url: The podcast URL
        :param int retention: The retention in days

        :return: The podcast instance
        :rtype: Podcast
        '''
        LOGGER.info('Creating new podcast from %r', url)

        title         = cls.parse_feed_url(url).feed.title
        podcast_dir   = pathlib.Path(podcasts_dir / title)
        metadata_file = podcast_dir / cls.metadata_filename

        if not podcast_dir.exists():
            podcast_dir.mkdir()

        if metadata_file.exists():
            LOGGER.warning('Podcast metadata file %r is already existing', metadata_file)
        else:
            with metadata_file.open(mode='w', encoding='utf-8') as file:
                json.dump({
                    'url': url,
                    'title': title,
                    'retention': retention or DEFAULT_RETENTION,
                }, file)

        return cls(podcast_dir)

    def __init__(self, podcast_dir):
        '''
        Constructor.
        '''
        LOGGER.debug('Initialising podcast at %r', podcast_dir)

        self.podcast_dir      = podcast_dir
        self.metadata_file    = podcast_dir / self.metadata_filename
        self.metadata         = {}
        self.current_download = None

        self.load_metadata()

    def __str__(self):
        '''
        The informal string representation of the podcast.

        :return: The title
        :rtype: str
        '''
        return self.metadata['title']

    def __repr__(self):
        '''
        The official string representation of the podcast.

        :return: The class w/ title
        :rtype: str
        '''
        return f'<{self.__class__.__name__}: {self.metadata["title"]}>'

    @property
    def info(self):
        '''
        The informations of the podcasts.

        :return: The filename & title
        :rtype: generator
        '''
        for file in self.podcast_dir.iterdir():
            if not file.name.startswith('.'):
                yield file.stem

    def load_metadata(self):
        '''
        Load the metadata from disk.
        '''
        LOGGER.debug('Loading metadata from %r', self.metadata_file)

        with self.metadata_file.open(mode='r', encoding='utf-8') as file_handle:
            self.metadata = json.load(file_handle)

    def save_metadata(self):
        '''
        Save the metadata to disk.
        '''
        LOGGER.debug('Saving metadata to %r', self.metadata_file)

        with open(self.metadata_file, 'w', encoding='utf-8') as file_handle:
            json.dump(self.metadata, file_handle)

    def clean(self, retention=None):
        '''
        Clean all podcast episodes which are older than the retention.

        :param retention: An alternative retention in days
        :type retention: None or int
        '''
        retention = retention or self.metadata.get('retention', DEFAULT_RETENTION)
        threshold = datetime.datetime.now() - datetime.timedelta(days=retention)

        for file in self.podcast_dir.iterdir():
            match = re.search(r'\d{4}(-\d{2}){2} \d{2}:\d{2}', file)
            if match:
                if datetime.datetime.strptime(match.group(0), '%Y-%m-%d %H:%M') < threshold:
                    LOGGER.info('Deleting %r', file)
                    (self.podcast_dir / file).unlink()
                else:
                    LOGGER.debug('Not deleteing %r because it\'s within the retention', file)
            else:
                LOGGER.debug('Ignoring %r because filename doesn\'t match', file)

    def set_retention(self, retention):
        '''
        Set a new retention.

        :param int retention: The retention in days
        '''
        LOGGER.info('Setting retention of %r to %d days', self, retention)
        self.metadata['retention'] = retention
        self.save_metadata()

    def download(self, retention=None, verify=False):  # pylint: disable=too-many-locals
        '''
        Download all episodes which are within the retention days.

        :param retention: An alternative retention in days
        :type retention: None or int
        :param bool verify: Verify the file size and redownload if missmatch
        '''
        LOGGER.info('Updating podcast %r', self.metadata['title'])

        retention       = retention or self.metadata.get('retention', DEFAULT_RETENTION)
        threshold_naive = datetime.datetime.now() - datetime.timedelta(days=retention)
        threshold_aware = datetime.datetime.now(tz=TIMEZONE) - datetime.timedelta(days=retention)
        feed            = self.parse_feed_url(self.metadata['url'])

        self.metadata['title'] = feed.feed.title

        for entry in feed.entries:  # pylint: disable=no-member
            title     = entry.title
            published = email.utils.parsedate_to_datetime(entry.published)
            links     = [link for link in entry.links if link.type in self.accepted_types]
            threshold = threshold_naive if published.tzinfo is None else threshold_aware

            if published < threshold:
                LOGGER.debug('Ignoring %r because it\'s older than %d days', title, retention)
                continue

            if not links:
                LOGGER.debug('Ignoring %r because no acceptable link types found', title)
                continue

            link      = links[0].href
            suffix    = os.path.splitext(urllib.parse.urlparse(link).path)[1]
            date_str  = published.strftime('%Y-%m-%d %H:%M')
            file_name = f'{date_str} - {title}{suffix}'
            file_path = self.podcast_dir / file_name
            exists    = file_path.exists()

            if not verify and exists:
                LOGGER.debug('Ignoring %r because it\'s already existing', title)
                continue

            with urllib.request.urlopen(link) as response:  # nosemgrep
                if exists and int(response.headers['content-length']) == file_path.stat.st_size:
                    LOGGER.debug(
                        'Ignoring %r because it\'s already existing and filesize matches', title)
                    continue
                if exists:
                    LOGGER.warning('Redownloading %r as the file size missmatches', title)
                else:
                    LOGGER.info('Downloading podcast episode %r', title)
                    LOGGER.debug('Podcast filename is %r', file_path)

                with file_path.open(mode='wb') as file:
                    file.write(response.read())
