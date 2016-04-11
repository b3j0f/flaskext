"""Extension for the cache module."""

from flask.ext.cache import Cache

from .base import Extension

from b3j0f.conf import Category


class _Cache(Annotation):

    def __init__(
            self, method, timeout=None, entry=None, unless=None, *args, **kwargs
    ):

        super(_Cache, self).__init__(*args, **kwargs)

        self.method = method
        self.timeout = timeout
        self.entry = entry
        self.unless = unless

    def load(self, loader, extension):

        for target in self.targets:

            method = getattr(extension.principals, self.method)
            method(target, self.timeout, self.entry, self.unless)


class Cached(_Cache):
    """Annotation dedicated to bind a view on a model element."""

    def __init__(self, *args, **kwargs):

        super(Cached, self).__init__(
            method='cached', *args, **kwargs
        )

class Memoize(_Cache):
    """Annotation dedicated to bind a view on a model element."""

    def __init__(self, *args, **kwargs):

        super(Memoize, self).__init__(
            method='memoize', *args, **kwargs
        )


@Configurable(paths='etc/cache.conf', conf=Category(name='cache'))
class CacheExtension(Extension):
    """Extension for the cache package."""

    def __init__(self, *args, **kwargs):

        super(CacheExtension, self).__init__(*args, **kwargs)

        self.cache = Cache()

    def init(self, loader):

        self.cache.init_app(loader.app)
        loader.cache = self.cache

    def load(self, module, loader):

        items = []

        view = getattr(module, 'view', module)
        if view is not None:
            modelitems = vars(view).values()
            items += modelitems

        for item in items:

            identities = _Cache.get_annotations(item)

            for identity in identities:

                identity.load(loader=loader, extension=self)
