from flask_sijax import Sijax

from .base import Extension

from b3j0f.conf import Configurable
from b3j0f.annotation import Annotation


class Route(Annotation):

    def __init__(self, urls=None, *args, **kwargs):

        super(Route, self).__init__(*args, **kwargs)

        self.urls = urls

    def load(self, loader, extension):

        for target in self.targets:

            extension.sijax.route(target, *self.urls)


@Configurable(paths='etc/sijax.conf')
class SijaxExtension(Extension):
    """Extension for the sijax package."""

    def __init__(self, *args, **kwargs):

        super(SijaxExtension, self).__init__(*args, **kwargs)

        self.sijax = Sijax()

    def _load(self, module, loader):

        self.sijax.init_app(loader.app)

        items = []

        route = getattr(module, 'route', module)
        if route is not None:
            modelitems = vars(route).values()
            items += modelitems

        for item in items:

            routes = Route.get_annotations(item)

            for route in routes:

                route.load(loader)
