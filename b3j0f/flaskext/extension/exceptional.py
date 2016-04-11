from flask.ext.exceptional import Exceptional

from b3j0f.conf import Configurable, Category

from .base import Extension


@Configurable(paths='etc/exceptional.conf', conf=Category(name='exceptional'))
class ExceptionalExtension(Extension):

    def _load(self, module, loader):

        self.exceptional = Exceptional(loader.app)
        loader.exceptional = self.exceptional
