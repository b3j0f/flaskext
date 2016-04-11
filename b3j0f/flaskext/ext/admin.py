"""Extension for administration module."""

from .base import Extension

from b3j0f.conf import category, Parameter
from b3j0f.annotation import Annotation

from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView

from sqlalchemy import Model


class BindView(Annotation):
    """Annotation dedicated to bind a view on a model element."""

    def __init__(self, viewcls=None, params=None, *args, **kwargs):

        super(BindView, self).__init__(*args, **kwargs)

        self.viewcls = viewcls
        self.params = {} if params is None else params

    def addview(self, loader, extension):

        viewcls = ModelView if self.viewcls is None else self.viewcls

        for target in self.targets:

            if issubclass(target, ModelView):
                view = target(**self.params)

            elif issubclass(target, Model):
                view = viewcls(target, loader.db.session, **self.params)

            elif isinstance(target, ModelView):
                view = target

            extension.add_view(view)


@Configurable(
    paths='etc/admin.conf',
    conf=category('admin', Parameter('index_view', ptype=AdminIndexView))
)
class AdminExtension(Extension):
    """Extension for the administration package."""

    def __init__(
            self, admin=None, app=None, name=None, url=None, subdomain=None,
            index_view=None, translations_path=None, endpoint=None,
            static_url_path=None, base_template=None, template_mode=None,
            category_icon_classes=None, *args, **kwargs
    ):

        super(AdminExtension, self).__init__(*args, **kwargs)

        self.admin = Admin(
            app=app, name=name, url=url, subdomain=subdomain,
            index_view=index_view, translations_path=translations_path,
            endpoint=endpoint, static_url_path=static_url_path,
            base_template=base_template, template_mode=template_mode,
            category_icon_classes=category_icon_classes
        ) if admin is None else admin

    def init_loader(self, loader):

        self.admin.init_app(loader.app)
        loader.admin = self.admin

    def load(self, module, loader):

        items = []

        model = getattr(module, 'model', module)
        if model is not None:
            modelitems = vars(model).values()
            items += modelitems

        view = getattr(module, 'view', None)
        if view is not None:
            viewitems = vars(view).values()
            items += viewitems

        for item in items:

            bindviews = BindView.get_annotations(item)

            for bindview in bindviews:

                bindview.addview(loader=loader, extension=self)
