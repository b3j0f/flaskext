from flask.ext.exceptional import Exceptional

from b3j0f.conf import Configurable, Category

from .base import Extension


@Configurable(paths='etc/exceptional.conf', conf=Category(name='exceptional'))
class ExceptionalExtension(Extension):

    def __init__(self, *args, **kwargs):

        super(ExceptionalExtension, self).__init__(*args, **kwargs)

        self.exceptional = Exceptional()

    def init(self, loader):

        self.exceptional.init_app(loader.app)
        loader.exceptional = self.exceptional
