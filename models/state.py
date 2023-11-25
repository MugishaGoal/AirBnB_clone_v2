#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Table, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv
import models


class State(BaseModel, Base):
    """State class"""
    __tablename__ = 'states'

    name = Column(String(128), nullable=False)
    
    # For DBStorage
    cities = relationship("City", cascade='all, delete', back_populates="state")

    # For FileStorage
    @property
    def cities(self):
        """Getter attribute for cities in FileStorage"""
        from models import storage
        city_list = []
        for city in storage.all(City).values():
            if city.state_id == self.id:
                city_list.append(city)
        return city_list
