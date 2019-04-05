from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Movies(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    movie_type = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return 
        {
            'movie_type': self.movie_type,
            'id': self.id,
        }


class Movie_item(Base):
    __tablename__ = 'movie_item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    producer = Column(String(250))
    starring = Column(String(250))
    movie_type_id = Column(Integer, ForeignKey('movies.id'))
    movies = relationship(Movies)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return 
        {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'producer': self.producer,
            'starring': self.starring,
        }


engine = create_engine('sqlite:///moviescatalogappwithlogin.db')


Base.metadata.create_all(engine)