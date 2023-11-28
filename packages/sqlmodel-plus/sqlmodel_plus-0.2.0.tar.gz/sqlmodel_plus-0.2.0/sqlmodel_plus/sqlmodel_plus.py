from typing import Any, Dict, Tuple, Union

from sqlalchemy.engine import Engine
from sqlmodel import Session, SQLModel, select, text
from sqlmodel.sql.expression import SelectOfScalar


class EngineException(Exception):
    pass


class SQLModelPlus(SQLModel):
    __engines__: Dict[str, Engine] = {}

    @classmethod
    @property
    def __get_scope(cls) -> str:
        return str(cls.__scope__) if hasattr(cls, "__scope__") else "default"

    @classmethod
    def create_tables(cls, *args, **kwargs):
        cls.metadata.create_all(cls.__engines__.get(cls.__get_scope), *args, **kwargs)

    @classmethod
    def find_by_id(cls, ident: Union[Dict[str, Any], Tuple[Any], Any]):
        with cls.Session as session:
            return session.get(cls, ident)

    def save(self):
        try:
            return self.create()
        except:
            return self.update()

    def create(self):
        with self.__class__.Session as session:
            session.add(self)
            session.commit()
            session.refresh(self)

        return self

    def update(self):
        with self.__class__.Session as session:
            updated_instance = session.merge(self)
            session.commit()
            session.refresh(updated_instance)

        return updated_instance

    def delete(self):
        with self.__class__.Session as session:
            session.delete(self)
            session.commit()

        return self

    @classmethod
    def set_engine(cls, engine: Engine) -> None:
        cls.__engines__[cls.__get_scope] = engine

    @classmethod
    def query(
        cls,
        statement: Union[SelectOfScalar, str],
        params: Union[Dict[str, Any], Tuple[Any]] = {},
    ):
        return Query(model_cls=cls, statement=statement, params=params)

    @classmethod
    @property
    def __db_session(cls):
        engine: Engine | None = cls.__engines__.get(cls.__get_scope)
        if engine is None:
            raise EngineException(
                "Engine is not initialized. Use `.set_engine` method to set engine."
            )

        return Session(bind=engine)

    @classmethod
    @property
    def select(cls) -> SelectOfScalar:
        return select(cls)

    @classmethod
    @property
    def Session(cls):
        return cls.__db_session


class Query:
    def __init__(
        self,
        model_cls: SQLModelPlus,
        statement: Union[SelectOfScalar, str],
        params: Union[Dict[str, Any], Tuple[Any], None] = None,
    ):
        self.model_cls = model_cls
        self.statement = (
            statement if isinstance(statement, SelectOfScalar) else text(statement)
        )
        self.params = params

    @property
    def all(self):
        with self.model_cls.Session as session:
            return session.exec(self.statement, params=self.params).all()

    @property
    def first(self):
        with self.model_cls.Session as session:
            return session.exec(self.statement, params=self.params).first()


__all__ = ["SQLModelPlus", "EngineException"]
