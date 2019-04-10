from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Movies, Base, Movie_item, User

engine = create_engine('sqlite:///moviescatalogappwithlogin.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

movietype1 = Movies(id=0, movie_type="Romantic")
session.add(movietype1)
session.commit()

movie1 = Movie_item(name="titanic", description="Titanic is a 1997 Ame\
    rican epic romance and disaster film", producer="James\
     Cameron", starring="Leonardo DiCaprio as Jack\
      Dawson", movies=movietype1, movie_type_id=0)
session.add(movie1)
session.commit()

movie2 = Movie_item(name="Ae dil hai mushkil", description="This movie\
 is based on love triangle", producer="Karan \
 Johar", starring="Ranbir Kapoor", movies=movietype1, movie_type_id=0)
session.add(movie2)
session.commit()

movietype2 = Movies(id=1, movie_type="Adventure")
session.add(movietype2)
session.commit()

movie3 = Movie_item(name="Avengers : Infinity Wars", description="Avengers \
    Infinity War is a 2018 American superhero \
    film based on the Marvel Comics superhero team Avengers", producer="\
    Marvel Studios", starring="Robert \
    Downey Jr. as Tony Stark Iron Man", movies=movietype2, movie_type_id=1)
session.add(movie3)
session.commit()

movie4 = Movie_item(name="Mowgli Legend of the Jungle", description="It is a \
    2018 adventure drama film", producer="Warner \
Bros. Pictures", starring="Rohan Chand \
as Mowgli", movies=movietype2, movie_type_id=1)
session.add(movie4)
session.commit()

movietype3 = Movies(id=2, movie_type="Fantasy")
session.add(movietype3)
session.commit()

movie5 = Movie_item(name="Fantastic Beasts The Crimes of \
    Grindelwald", description="It is a 2018 fantasy film directed\
     by David Yates and written by J. K. Rowling.\
     ", producer="Warner Bros. Pictures", starring="Eddie \
     Redmayne as Newt Scamander", movies=movietype3, movie_type_id=2)
session.add(movie5)
session.commit()

print "all movies added"
