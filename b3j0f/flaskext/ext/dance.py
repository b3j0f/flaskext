from b3j0f.conf import Configurable

from .base import Extension

from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from flask_dance.contrib.dropbox import make_dropbox_blueprint, dropbox
from flask_dance.contrib.meetup import make_meetup_blueprint, meetup
from flask_dance.contrib.slack import make_slack_blueprint, slack


@Configurable(paths='etc/dance.conf')
class DanceExtension(Extension):

    def __init__(self, entries, *args, **kwargs):

        super(DanceExtension, self).__init__(*args, **kwargs)

        self.entries = entries

    def init(self, loader):

        for entry in self.entries:

            params = self.entries[entry]

            make_blueprint = globals()['make_{0}_blueprint'.format(entry)]

            blueprint = make_blueprint(**params)

            url_prefix = '/login/{0}'.format(entry)
            loader.app.register_blueprint(blueprint, url_prefix=url_prefix)
