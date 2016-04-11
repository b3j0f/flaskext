"""Extension for the principal module."""

from .base import Extension

from b3j0f.conf import Category
from b3j0f.annotation import Annotation

from flask.ext.principal import Principal


class _Identity(Annotation):

    def __init__(self, method, *args, **kwargs):

        super(_Identity, self).__init__(*args, **kwargs)

        self.method = method

    def load(self, loader, extension):

        for target in self.targets:

            method = getattr(extension.principals, self.method)
            method(target)


class IdentityLoader(_Identity):
    """Annotation dedicated to bind a view on a model element."""

    def __init__(self, *args, **kwargs):

        super(IdentityLoader, self).__init__(
            method='identity_loader', *args, **kwargs
        )

class IdentitySaver(_Identity):
    """Annotation dedicated to bind a view on a model element."""

    def __init__(self, *args, **kwargs):

        super(IdentitySaver, self).__init__(
            method='identity_saver', *args, **kwargs
        )


@Configurable(paths='etc/principal.conf', conf=Category(name='principal'))
class PrincipalExtension(Extension):
    """Extension for the principal package."""

    def __init__(self, *args, **kwargs):

        super(PrincipalExtension, self).__init__(*args, **kwargs)

        self.principal = Principal()

    def init(self, loader):

        self.principal.init_app(loader.app)
        loader.principal = self.principal

    def load(self, module, loader):

        items = []

        acl = getattr(module, 'acl', module)
        if acl is not None:
            modelitems = vars(acl).values()
            items += modelitems

        for item in items:

            identities = _Identity.get_annotations(item)

            for identity in identities:

                identity.load(loader=loader, extension=self)
