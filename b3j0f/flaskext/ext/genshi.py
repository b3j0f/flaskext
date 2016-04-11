"""Extension for the genshi module."""

from flaskext.genshi import Genshi

from .base import Extension

from b3j0f.conf import Category


class Filter(Annotation):

    def load(self, loader, extension):

        for target in self.targets:

            extension.genshi.filter(target)


@Configurable(paths='etc/genshi.conf', conf=Category(name='genshi'))
class GenshiExtension(Extension):
    """Extension for the genshi package."""

    def __init__(self, *args, **kwargs):

        super(GenshiExtension, self).__init__(*args, **kwargs)

        self.genshi = Genshi()

    def init(self, loader):

        self.genshi.init_app(loader.app)
        loader.genshi = self.genshi

    def load(self, module, loader):

        items = []

        view = getattr(module, 'view', module)
        if view is not None:
            modelitems = vars(view).values()
            items += modelitems

        for item in items:

            filters = Filter.get_annotations(item)

            for filt in filters:

                filt.load(loader=loader, extension=self)
