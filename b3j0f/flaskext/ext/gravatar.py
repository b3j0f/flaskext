from flask.ext.gravatar import Gravatar

from b3j0f.conf import Configurable, category, Parameter, BOOL

from .base import Extension


@Configurable(
    paths='etc/gravatar.conf',
    conf=category(
        'gravatar',
        Parameter('size', ptype=int, value=100),
        Parameter('rating', value='g'),
        Parameter('default', value='retro'),
        Parameter('force_default', ptype=BOOL, value=False),
        Parameter('force_lower', ptype=BOOL, value=False),
        Parameter('use_ssl', ptype=BOOL, value=False)
    )
)
class GravatarExtension(Extension):

    def __init__(
            self, size=None, rating=None, default=None, force_default=False,
            force_lower=False, use_ssl=False, base_url=None, *args, **kwargs
    ):

        super(GravatarExtension, self).__init__(*args, **kwargs)

        self.size = size
        self.rating = rating
        self.default = default
        self.force_default = force_default
        self.force_lower = force_lower
        self.use_ssl = use_ssl
        self.base_url = base_url

    def init(self, loader):

        loader.gravatar = Gravatar(
            loader.app,
            size=self.size,
            rating=self.rating,
            default=self.default,
            force_default=self.force_default,
            force_lower=self.force_lower,
            use_ssl=self.use_ssl,
            base_url=self.base_url
        )
