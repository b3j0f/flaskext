from b3j0f.conf import Configurable, Parameter, Array

from flask import Flask, Blueprint

from types import ModuleType

from .extension.base import Extension


@Configurable(
    paths='etc/loader.conf',
    conf=[
        Parameter('extensions', ptype=Array(Extension)),
        Parameter('modules', ptype=Array(ModuleType))
    ]
)
class Loader(object):
    """Class dedicated to load a flask website application."""

    def __init__(
            self, app=None, host=None, port=None,
            import_name=None, static_url_path=None, static_folder=None,
            template_folder=None, instance_path=None,
            instance_relative_config=None,
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

        self.host = host
        self.port = port

        self.modules = modules
        self.extensions = extensions

    def loadmodules(self):

        for module in self.modules:

            blueprint = getattr(module, 'blueprint', module)

            if blueprint is not None:
                content = vars(blueprint).values()

                if isinstance(content, Blueprint):
                    self.app.register_blueprint(content)

            for extension in self.extensions:

                extension.load(module=module, loader=self)

    def run(self, host, port):

        if host is None:
            host = self.host

        if port is None:
            port = self.port

        self.loadmodules()

        self.app.run(host=host, port=port)
