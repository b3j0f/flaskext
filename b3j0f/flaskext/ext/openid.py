from flask.ext.openid import OpenID

from .base import Extension

from b3j0f.conf import category, Parameter, Array


@Configurable(
    paths='etc/openid.conf',
    conf=category(
        'openid',
        Parameter(name='extension_responses', ptype=Array(type))
    )
)
class OpenIDExtension(Extension):
    """Extension for the openid package."""

    def __init__(
            self, fs_store_path=None, store_factory=None,
            fallback_endpoint=None, extension_responses=None, safe_roots=None,
            url_root_as_trust_root=False, *args, **kwargs
    ):

        super(OpenIDExtension, self).__init__(*args, **kwargs)

        self.openid = OpenID(
            fs_store_path=fs_store_path, store_factory=store_factory,
            fallback_endpoint=fallback_endpoint,
            extension_responses=extension_responses, safe_roots=safe_roots,
            url_root_as_trust_root=url_root_as_trust_root
        )

    def init(self, loader):

        self.openid.init_app(loader.app)
