"""Extension for the stormpath module."""

from flask.ext.stormpath import StormpathManager

from .base import Extension

from b3j0f.conf import Category



@Configurable(paths='etc/stormpath.conf', conf=Category(name='stormpath'))
class PrincipalExtension(Extension):
    """Extension for the stormpath package."""

    def __init__(self, *args, **kwargs):

        super(PrincipalExtension, self).__init__(*args, **kwargs)

        self.stormpath = StormpathManager()

    def _load(self, module, loader):

        self.stormpath.init_app(loader.app)
        loader.stormpath = self.stormpath
