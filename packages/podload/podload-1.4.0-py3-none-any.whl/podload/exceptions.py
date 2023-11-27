'''
Podload exceptions module.
'''


class PodloadError(Exception):
    '''
    Exception which is thrown when a podload error occurs.
    '''


class FeedError(PodloadError):
    '''
    Exception which is thrown when a feed or parsing error occurs.
    '''


class PodcastNotFoundError(PodloadError):
    '''
    Exception which is thrown when a podcast with a certain title wasn't found.
    '''
