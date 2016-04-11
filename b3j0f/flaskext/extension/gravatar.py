from flask.ext.gravatar import Gravatar

from b3j0f.conf import Configurable, Category

from .base import Extension


@Configurable(paths='etc/gravatar.conf', conf=Category(name='gravatar'))
class GravatarExtension(Extension):

    def __init__(
        self, size=None, rating=None, default=None, force_default=False,
        force_lower=False, use_ssl=False, base_url=None, *args, **kwargs
    ):

        super(GravatarExtension, self).__init__(*args, **kwargs)

        self.size = size
        self.rating = rating,
        self.default = default
        self.force_default = force_default
        self.force_lower = force_lower
        self.use_ssl = use_ssl
        self.base_url = base_url

    def _load(self, module, loader):

        self.gravatar = Gravatar(loader.app)
        loader.gravatar = self.gravatar
