from flask_mail import Mail

from b3j0f.conf import Configurable, category, Parameter, BOOL

from .base import Extension


@Configurable(
    paths='etc/mail.conf',
    conf=category(
        'mail',
        Parameter('port', ptype=int),
        Parameter('use_tls', ptype=BOOL),
        Parameter('use_ssl', ptype=BOOL),
        Parameter('debug', ptype=BOOL),
        Parameter('max_emails', ptype=int),
        Parameter('suppress_send', ptype=BOOL)
    )
)
class MailExtension(Extension):

    def __init__(
            self, server=None, port=None, use_tls=None, use_ssl=None,
            debug=None, username=None, password=None, default_sender=None,
            max_emails=None, suppress_send=None, ascii_attachments=None,
            *args, **kwargs
    ):

        super(MailExtension, self).__init__(*args, **kwargs)

        self.mail = Mail()
        self.server = server
        self.port = port
        self.use_tls = use_tls
        self.use_ssl = use_ssl
        self.debug = debug
        self.username = username
        self.password = password
        self.default_sender = default_sender
        self.max_emails = max_emails
        self.suppress_send = suppress_send
        self.ascii_attachments = ascii_attachments

    @property
    def config(self):

        return {
            'MAIL_SERVER': self.server,
            'MAIL_PORT': self.port,
            'MAIL_USE_TLS': self.use_tls,
            'MAIL_USE_SSL': self.use_ssl,
            'MAIL_DEBUG': self.debug,
            'MAIL_USERNAME': self.username,
            'MAIL_PASSWORD': self.password,
            'MAIL_DEFAULT_SENDER': self.default_sender,
            'MAIL_MAX_EMAILS': self.max_emails,
            'MAIL_SUPPRESS_SEND': self.suppress_send,
            'MAIL_ASCII_ATTACHMENTS': self.ascii_attachments
        }

    def init(self, loader):

        loader.app.config.update(self.config)
        self.mail = self.mail.init_app(loader.app)
        loader.mail = self.mail
