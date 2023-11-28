# SQLModel Plus

[![GitHub license badge](badges/badge-license.svg)](http://www.apache.org/licenses/LICENSE-2.0)
[![Coverage](badges/coverage.svg)]()
[![pypi](https://img.shields.io/pypi/v/sqlmodel-plus.svg)](https://pypi.python.org/pypi/sqlmodel-plus)

## Installation

Install package using pip -> `pip install sqlmodel-plus`

## Usage

Use `SQLModelPlus` class to define data models and tables as it inherits `SQLModel`. \
To use in-built functions, an engine needs to set using `set_engine` method.

```python
from sqlmodel_plus import SQLModelPlus, EngineException
from typing import Optional
from sqlmodel import Field, SQLModel, create_engine

class Hero(SQLModelPlus, table=True):
    __tablename__ = "hero"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None

SQLModelPlus.set_engine(create_engine(f"sqlite:///database.db"))
```

If engine is not set it will raise `EngineException`

By using `SQLModelPlus` class, it provide following classmethods available to all inherited classes -

#### find_by_id

```python
Hero.find_by_id(1)
Hero.find_by_id("uuid")
Hero.find_by_id((1, 2,))
Hero.find_by_id({"id": 1, "version": 3})
```

#### save

Create or Update Record in database.
```python
hero = Hero(id=1, name="hero_1", secret_name="Secret_hero").save()
hero.name = "hero_2"
hero.save()

```

#### create

Create new record in database.
```python
Hero(id=1, name="hero_1", secret_name="Secret_hero").create()
```

#### update

Update record in database.
```python
hero = Hero(id=1, name="hero_1", secret_name="Secret_hero")
hero.name = "hero_2"
hero.update()
```

#### delete

Delete record from database
```python
hero = Hero(id=1, name="hero_1", secret_name="Secret_hero").save()
hero.delete()
```

#### select

```python
statement = Hero.select  # This is equivalant to select(Hero)
statement.where(Hero.id == 1)
```

#### query

```python
statement = Hero.select.where(Hero.id == 1)
Hero.query(statement).all
Hero.query("SELECT id FROM hero").first
```

#### Session

```python
session = Hero.Session # Return Session object
session.exec(Hero.select).all()

with Hero.Session as session:
    session.exec(Hero.select.where(Hero.id == 1)).first()
```

#### create_tables

Create tables in database. \
It is equivalant of `SQLModel.metadata.create_all` method where you don't need to provide bind parameter.
```python
SQLModelPlus.create_tables()
```
