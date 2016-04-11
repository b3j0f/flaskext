from flask_mail import Mail

from b3j0f.conf import Configurable, Category

from .base import Extension


@Configurable(paths='etc/mail.conf', conf=Category(name='mail'))
class MailExtension(Extension):

    def __init__(
        self, size=None, rating=None, default=None, force_default=False,
        force_lower=False, use_ssl=False, base_url=None, *args, **kwargs
    ):

        super(MailExtension, self).__init__(*args, **kwargs)

        self.mail = Mail()

    def _load(self, module, loader):

        self.mail = self.mail.init_app(loader.app)
        loader.mail = self.mail
