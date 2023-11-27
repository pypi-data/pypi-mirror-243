from typing import Optional

from aipkgs_core.utils.singleton import Singleton
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


def initialize(db: SQLAlchemy) -> SQLAlchemy:
    DatabaseCore.shared.initialize(db=db)
    return DatabaseCore.shared.db


def db() -> SQLAlchemy:
    return DatabaseCore.shared.db