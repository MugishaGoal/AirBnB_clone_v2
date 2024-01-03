#!/usr/bin/python3
"""New class for SQLAlchemy """
import os
from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """Creates tables in an environmental database using SQLAlchemy"""

    __engine = None
    __session = None

    def __init__(self):
        """Initializes the database connection"""
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        db = getenv("HBNB_MYSQL_DB")
        host = getenv("HBNB_MYSQL_HOST")
        env = getenv("HBNB_ENV")

        if not all((user, passwd, db, host, env)):
            raise EnvironmentError("Missing required environment variables")

        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}:3306/{}"
                                      .format(user, passwd, host, db),
                                      pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of objects"""
        dic = {}
        if cls:
            if isinstance(cls, str):
                cls = eval(cls)
            query = self.__session.query(cls)
            for elem in query:
                key = "{}.{}".format(type(elem).__name__, elem.id)
                dic[key] = elem
        else:
            classes = [State, City, User, Place, Review, Amenity]
            for class_ in classes:
                query = self.__session.query(class_)
                for elem in query:
                    key = "{}.{}".format(type(elem).__name__, elem.id)
                    dic[key] = elem
        return dic

    def new(self, obj):
        """Adds a new element to the table"""
        self.__session.add(obj)

    def save(self):
        """Saves changes"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes an element from the table"""
        if obj:
            self.__session.delete(obj)
            self.save()

    def reload(self):
        """Configures and reloads the session"""
        Base.metadata.create_all(self.__engine)
        sec = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sec)
        self.__session = Session()

    def close(self):
        """Terminates the session"""
        self.__session.close()


"""Set the required environment variables"""
os.environ['HBNB_MYSQL_USER'] = 'hbnb_dev'
os.environ['HBNB_MYSQL_PWD'] = 'hbnb_dev_pwd'
os.environ['HBNB_MYSQL_HOST'] = 'localhost'
os.environ['HBNB_MYSQL_DB'] = 'hbnb_dev_db'
os.environ['HBNB_ENV'] = 'development'

"""Now create an instance of DBStorage"""
storage = DBStorage()
storage.reload()
