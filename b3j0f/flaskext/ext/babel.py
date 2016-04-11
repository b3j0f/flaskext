"""Extension for the babel module."""

from flask.ext.babel import Babel

from .base import Extension

from b3j0f.conf import category, Parameter, BOOL
from b3j0f.annotation import Annotation


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


@Configurable(
    paths='etc/babel.conf',
    conf=category('babel', Parameter(name='configure_jinja', ptype=BOOL))
)
class BabelExtension(Extension):
    """Extension for the babel package."""

    def __init__(
            self, default_locale=None, default_timezone=None, date_formats=None,
            configure_jinja=None, *args, **kwargs
    ):

        super(BabelExtension, self).__init__(*args, **kwargs)

        self.babel = Babel(
            default_locale=default_locale, default_timezone=default_timezone,
            date_formats=date_formats, configure_jinja=configure_jinja
        )

    def init(self, loader):

        self.babel.init_app(loader.app)
        loader.babel = self.babel

    def load(self, module, loader):

        items = []

        lang = getattr(module, 'lang', module)
        if lang is not None:
            modelitems = vars(lang).values()
            items += modelitems

        for item in items:

            selector = _Selector.get_annotations(item)

            for identity in selector:

                identity.load(loader=loader, extension=self)
