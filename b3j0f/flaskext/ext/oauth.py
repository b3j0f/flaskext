from flask_oauth import OAuth

from .base import Extension

from b3j0f.conf import category, Parameter, Array


@Configurable(
    paths='etc/oauth.conf',
    conf=category(
        'oauth',
        Parameter(name='remotes', ptype=Array(dict))
    )
)
class OAuthExtension(Extension):
    """Extension for the oauth package."""

    def __init__(self, remotes=None, *args, **kwargs):

        super(OAuthExtension, self).__init__(*args, **kwargs)

        self.oauth = OAuth()

        self.remotes = remotes

    def init(self, loader):

        if self.remotes:
            for remote in self.remotes:

                self.oauth.remote_app(**remote)
