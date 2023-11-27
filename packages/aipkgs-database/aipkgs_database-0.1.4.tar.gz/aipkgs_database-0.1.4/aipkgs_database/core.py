from typing import Optional

from aipkgs_core.utils.singleton import Singleton
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


@Singleton
class DatabaseCore:
    def __init__(self):
        self.__db: Optional[SQLAlchemy] = None

    @property
    def db(self) -> Optional[SQLAlchemy]:
        return self.__db

    def __initialize(self, db: SQLAlchemy):
        self.__db = db

    def initialize(self, db: SQLAlchemy):
        self.__initialize(db=db)

    def create_tables(app: Flask) -> bool:
        with app.app_context():
            db: SQLAlchemy = DatabaseCore.shared.db()
            if db is None:
                return False

            db.create_all()
            return True


def initialize(db: SQLAlchemy) -> SQLAlchemy:
    DatabaseCore.shared.initialize(db=db)
    return DatabaseCore.shared.db


def db() -> SQLAlchemy:
    return DatabaseCore.shared.db


def create_tables(app: Flask) -> bool:
    return DatabaseCore.shared.create_tables(app=app)
