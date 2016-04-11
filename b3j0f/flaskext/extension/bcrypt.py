"""Extension for the bcrypt module."""

from flask.ext.bcrypt import Bcrypt

from .base import Extension

from b3j0f.conf import Category


@Configurable(paths='etc/bcrypt.conf', conf=Category(name='bcrypt'))
class BCryptExtension(Extension):
    """Extension for the bcrypt package."""

    def __init__(self, *args, **kwargs):

        super(BCryptExtension, self).__init__(*args, **kwargs)

        self.bcrypt = Bcrypt()

    def _load(self, module, loader):

        self.bcrypt.init_app(loader.app)
        loader.bcrypt = self.bcrypt
