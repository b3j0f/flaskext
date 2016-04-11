from flask_sqlalchemy import SQLAlchemy

from b3j0f.conf import Configurable

from .base import Extension


@Configurable(paths='etc/sqlalchemy.conf')
class SQLAlchemyExtension(Extension):

    def _load(self, module, loader):

        self.db = SQLAlchemy(loader.app)
        loader.db = self.db
