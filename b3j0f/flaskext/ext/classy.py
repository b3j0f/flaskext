from flask.ext.classy import FlaskView

from b3j0f.conf import Configurable

from .base import Extension


@Configurable(paths='etc/classy.conf')
class ClassyExtension(Extension):

    def load(self, module, loader):

        view = getattr(module, 'view', module)

        items = vars(view).values()

        for item in items:

            if isinstance(item, FlaskView):
                item.register(loader.app)
