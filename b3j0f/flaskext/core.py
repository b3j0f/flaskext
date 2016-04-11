from b3j0f.utils.path import lookup
from b3j0f.conf import Configurable, Parameter, Array, category, BOOL

from flask import Flask, Blueprint

from .extension.base import Extension

from datetime import timedelta


@Configurable(
    paths='etc/loader.conf',
    conf=category(
        'loader',
        Parameter(name='host', value='0.0.0.0'),
        Parameter(name='port', value=5000, ptype=int),
        Parameter('extensions', ptype=Array(Extension)),
        Parameter('modules', ptype=Array()),
        Parameter('static_folder', value='static'),
        Parameter('template_folder', value='templates'),
        Parameter('instance_folder', value='instance'),
        Parameter('instance_relative_config', value=True, ptype=BOOL),
        Parameter('config', ptype=dict, value={
            'JSON_AS_ASCII': True, 'USE_X_SENDFILE': False,
            'SESSION_COOKIE_PATH': None, 'SESSION_COOKIE_DOMAIN': None,
            'SESSION_COOKIE_NAME': 'session', 'LOGGER_NAME': None,
            'DEBUG': False, 'SECRET_KEY': None, 'MAX_CONTENT_LENGTH': None,
            'APPLICATION_ROOT': None, 'SERVER_NAME': None,
            'PREFERRED_URL_SCHEME': 'http', 'JSONIFY_PRETTYPRINT_REGULAR': True,
            'TESTING': False, 'PROPAGATE_EXCEPTIONS': None,
            'TRAP_BAD_REQUEST_ERRORS': False, 'JSON_SORT_KEYS': True,
            'SESSION_COOKIE_HTTPONLY': True, 'SEND_FILE_MAX_AGE_DEFAULT': 43200,
            'PRESERVE_CONTEXT_ON_EXCEPTION': None,
            'SESSION_COOKIE_SECURE': False, 'TRAP_HTTP_EXCEPTIONS': False,
            'PERMANENT_SESSION_LIFETIME': timedelta(31)
        })
    )
)
class Loader(object):
    """Class dedicated to load a flask website application."""

    def __init__(
            self, app=None, host=None, port=None,
            import_name=None, static_url_path=None, static_folder=None,
            template_folder=None, instance_path=None,
            instance_relative_config=None, config=None,
            modules=None, extensions=None, *args, **kwargs
    ):

        super(Loader, self).__init__(*args, **kwargs)

        if import_name is None:
            import_name = __name__

        self.app = Flask(
            import_name=import_name, static_url_path=static_url_path,
            static_folder=static_folder, template_folder=template_folder,
            instance_path=instance_path,
            instance_relative_config=instance_relative_config
        ) if app is None else app

        self.config = config

        self.app.config.update(config)

        self.host = host
        self.port = port

        self.modules = modules
        self.extensions = extensions

        import app

        app.loader = self

    def init_extensions(self):

        for extension in self.extensions:

            extension.init_loader(self)

    def loadmodules(self):

        for module in self.modules:

            module = lookup(module)

            blueprint = getattr(module, 'blueprint', module)

            if blueprint is not None:
                content = vars(blueprint).values()

                if isinstance(content, Blueprint):
                    self.app.register_blueprint(content)

            for extension in self.extensions:

                extension.load(module=module, loader=self)

    def run_extensions(self):

        for extension in self.extensions:

            extension.run(loader=self)

    def run(self, host, port):
        """Run this loader in executing successivelly methods:

        - init_extensions
        - loadmodules
        - run_extensions
        - this app.

        :param str host: flask host to run.
        :param int port: flask port to run."""

        if host is None:
            host = self.host

        if port is None:
            port = self.port

        self.init_extensions()

        self.loadmodules()

        self.run_extensions()

        self.app.run(host=host, port=port)
