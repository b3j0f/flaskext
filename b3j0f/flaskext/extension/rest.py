from flask_restful import Resource, Api

from .base import Extension

from b3j0f.conf import Configurable
from b3j0f.annotation import Annotation


class AddResource(Annotation):

    def __init__(self, urls=None, *args, **kwargs):

        super(AddResource, self).__init__(*args, **kwargs)

        self.urls = urls

    def load(self, loader, extension):

        for target in self.targets:

            extension.api.add_resource(target, *self.urls)


@Configurable(paths='etc/rest.conf')
class LoginExtension(Extension):
    """Extension for the login package."""

    def __init__(self, *args, **kwargs):

        super(LoginExtension, self).__init__(*args, **kwargs)

        self.api = Api()

    def _load(self, module, loader):

        self.api.init_app(loader.app)

        items = []

        rest = getattr(module, 'rest', module)
        if rest is not None:
            modelitems = vars(rest).values()
            items += modelitems

        for item in items:

            addresources = AddResource.get_annotations(item)

            if addresources:
                for addresource in addresources:

                    addresource.load(loader)

            elif isinstance(item, Resource):
                self.api.add_resource(item)
