"""Extension for the babel module."""

from .base import Extension

from b3j0f.conf import Category
from b3j0f.annotation import Annotation

from flask.ext.babel import Principal


class _Selector(Annotation):

    def __init__(self, method, *args, **kwargs):

        super(_Selector, self).__init__(*args, **kwargs)

        self.method = method

    def load(self, loader, extension):

        for target in self.targets:

            method = getattr(extension.principals, self.method)
            method(target)


class LocaleSelector(_Selector):
    """Annotation dedicated to bind a view on a model element."""

    def __init__(self, *args, **kwargs):

        super(LocaleSelector, self).__init__(
            method='localeselector', *args, **kwargs
        )

class TimeZoneSelector(_Selector):
    """Annotation dedicated to bind a view on a model element."""

    def __init__(self, *args, **kwargs):

        super(TimeZoneSelector, self).__init__(
            method='timezoneselector', *args, **kwargs
        )


@Configurable(paths='etc/babel.conf', conf=Category(name='babel'))
class PrincipalExtension(Extension):
    """Extension for the babel package."""

    def __init__(self, *args, **kwargs):

        super(PrincipalExtension, self).__init__(*args, **kwargs)

        self.babel = Principal()

    def _load(self, module, loader):

        self.babel.init_app(loader.app)
        loader.babel = self.babel

        items = []

        lang = getattr(module, 'lang', module)
        if lang is not None:
            modelitems = vars(lang).values()
            items += modelitems

        for item in items:

            selector = _Selector.get_annotations(item)

            for identity in selector:

                identity.load(loader=loader, extension=self)
