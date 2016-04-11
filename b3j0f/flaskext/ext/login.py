"""Extension for the login module."""

from .base import Extension

from b3j0f.conf import Category
from b3j0f.annotation import Annotation

from flask.ext.login import LoginManager


class UserLoader(Annotation):
    """Annotation dedicated to bind a view on a model element."""

    def __init__(self, viewcls=None, params=None, *args, **kwargs):

        super(UserLoader, self).__init__(*args, **kwargs)

        self.viewcls = viewcls
        self.params = {} if params is None else params

    def load(self, loader, extension):

        for target in self.targets:

            extension.login.user_loader(target)


@Configurable(paths='etc/login.conf', conf=Category(name='login'))
class LoginExtension(Extension):
    """Extension for the login package."""

    def __init__(self, *args, **kwargs):

        super(LoginExtension, self).__init__(*args, **kwargs)

        self.login = LoginManager()

    def init(self, loader):

        self.login.init_app(loader.app)
        loader.login = self.login

    def load(self, module, loader):

        items = []

        login = getattr(module, 'login', module)
        if login is not None:
            modelitems = vars(login).values()
            items += modelitems

        for item in items:

            userloaders = UserLoader.get_annotations(item)

            for userloader in userloaders:

                userloader.load(loader=loader, extension=self)
