from flask_debugtoolbar import DebugToolbarExtension

from b3j0f.conf import Configurable, Category

from .base import Extension


@Configurable(paths='etc/debugtoolbar.conf', conf=Category(name='debugtoolbar'))
class DebugToolbarExtension(Extension):

    def init(self, loader):

        loader.debugtoolbar = DebugToolbarExtension(loader.app)
