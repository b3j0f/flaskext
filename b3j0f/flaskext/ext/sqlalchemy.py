from flask_sqlalchemy import SQLAlchemy

from b3j0f.conf import Configurable

from .base import Extension


@Configurable(paths='etc/sqlalchemy.conf')
class SQLAlchemyExtension(Extension):

    def __init__(self, *args, **kwargs):

        super(SQLAlchemyExtension, self).__init__(*args, **kwargs)

        self.db = SQLAlchemy()

    def load(self, module, loader):

        if self.db.get_app() is None:
            self.db.init_app(loader.app)
            loader.db = self.db

    def run(self, loader):

        self.db.create_all()
