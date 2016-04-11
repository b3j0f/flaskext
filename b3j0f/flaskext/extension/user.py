from flask_user import UserManager, UserMixin, SQLAlchemyAdapter

from .base import Extension

from b3j0f.conf import Category



@Configurable(paths='etc/user.conf', conf=Category(name='user'))
class UserExtension(Extension):
    """Extension for the user package."""

    def _load(self, module, loader):

        items = []

        model = getattr(module, 'model', module)
        if model is not None:
            modelitems = vars(model).values()
            items += modelitems

        for item in items:

            if isinstance(item, UserMixin):

                dbadapter = SQLAlchemyAdapter(loader.db, item)
                UserManager(dbadapter, loader.db)
