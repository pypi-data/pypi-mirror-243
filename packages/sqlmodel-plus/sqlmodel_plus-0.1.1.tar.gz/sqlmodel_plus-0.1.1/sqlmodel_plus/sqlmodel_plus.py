from sqlmodel import select, SQLModel, Session, text
from typing import Tuple, Dict, Any, Union
from sqlalchemy.engine import Engine
from sqlmodel.sql.expression import SelectOfScalar

class EngineException(Exception):
    pass

class SQLModelPlus(SQLModel):
    __engines__: Dict[str, Engine] = {}
    @classmethod
    @property
    def __get_scope(cls) -> str:
        return str(cls.__scope__ )if hasattr(cls, '__scope__') else "default"
        
    
    @classmethod
    def find_by_id(cls, ident: Union[Dict[str, Any], Tuple[Any], Any]):
        with cls.Session as session:
            return session.get(cls, ident)
    
    
    def save(self, instance):
        with self.__class__.Session as session:
            session.add(instance)
            session.commit(instance)
            session.refresh(instance)
            
        return instance
    
    def create(self, instance):
        return self.save(instance=instance)
    
    def update(self, instance):
        return self.save(instance=instance)
        
    
    @classmethod
    def set_engine(cls, engine: Engine) -> None:
        cls.__engines__[cls.__get_scope] = engine
        
    @classmethod
    def query(cls, statement: Union[SelectOfScalar, str], params: Union[Dict[str, Any], Tuple[Any]] = {}):
        return Query(model_cls=cls, statement=statement, params=params)
        
    @classmethod
    @property
    def __db_session(cls):
        engine: Engine | None = cls.__engines__.get(cls.__get_scope)
        if engine is None:
            raise EngineException('Engine is not initialized. Use `.set_engine` method to set engine.')
        
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
    def __init__(self, model_cls: SQLModelPlus, statement: Union[SelectOfScalar, str], params: Union[Dict[str, Any], Tuple[Any], None] = None):
        self.model_cls = model_cls
        self.statement = statement if isinstance(statement, SelectOfScalar) else text(statement)
        self.params = params
        
    @property
    def all(self):
        with self.model_cls.Session as session:
            return session.exec(self.statement, params=self.params).all()
        
    @property
    def first(self):
        with self.model_cls.Session as session:
            return session.exec(self.statement, params=self.params).first()
        
    @property
    def count(self) -> int:
        with self.model_cls.Session as session:
            return session.exec(self.statement, params=self.params).count()
        
__all__ = ['SQLModelPlus', 'EngineException']