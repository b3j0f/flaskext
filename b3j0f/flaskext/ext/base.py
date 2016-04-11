"""Base class for flask extensions."""


class Extension(object):
    """Base extension class which is dedicated to extend website resources with
    flask extensions.

    Examples are provided in other modules of this package."""

    def init(self, loader):
        """Called before loading modules.

        :param Loader loader: loader to initialize."""

    def load(self, module, loader):
        """Load a module.

        :param Module module: module to load.
        :param Loader loader: loader to load.."""

        raise NotImplementedError()

    def run(self, loader):
        """Run input loader."""
