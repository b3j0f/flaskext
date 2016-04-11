"""Base class for flask extensions."""


class Extension(object):
    """Base extension class which is dedicated to extend website resources with
    flask extensions.

    Examples are provided in other modules of this package."""

    def __init__(self, module=None, loader=None, *args, **kwargs):

        super(Extension, self).__init__(*args, **kwargs)

        self.module = module
        self.loader = loader

    def load(self, module=None, loader=None):
        """Load a module.

        :param Module module: module to load. Default is this module.
        :param Loader loader: loader to load. Default is this loader."""

        if module is None:
            module = self.module

        if loader is None:
            loader = self.loader

        self._load(module=module, loader=loader)

    def _load(self, module, loader):
        """Protected module loader to override.

        Internally called by self method load.

        :param Module module: module to load.
        :param Loader loader: loader to load."""

        raise NotImplementedError()
