from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base


BASE = declarative_base()


class People(BASE):
    """
    Model for all the people in the dojo
    """
    __tablename__ = "people"
    person_id = Column(Integer, primary_key=True)
    names = Column(String)
    person_type = Column(String)

    def __init__(self, person_id, names, person_type):
        self.person_id = person_id
        self.names = names
        self.person_type = person_type


class Rooms(BASE):
    """
    Model for all the rooms in the dojo
    """
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    room_name = Column(String)
    room_type = Column(String)
    room_capacity = Column(Integer)
    room_occupants = Column(String)

    def __init__(self, room_name, room_type, room_capacity, room_occupants):
        self.room_name = room_name
        self.room_type = room_type
        self.room_capacity = room_capacity
        self.room_occupants = room_occupants


class Unallocated(BASE):
    """
    Model for all the unallocated people in the dojo
    """
    __tablename__ = "unallocated"
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer)
    names = Column(String)
    person_type = Column(String)
    without_room = Column(String)

    def __init__(self, person_id, names, person_type, without_room):
        self.person_id = person_id
        self.names = names
        self.person_type = person_type
        self.without_room = without_room
