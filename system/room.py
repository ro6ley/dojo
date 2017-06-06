class Room(object):
    """Class to create a room object. Inherited by Office and LivingSpace"""

    def __init__(self, room_name=None, room_type=None, room_capacity=None,
                 room_occupants=[]):
        self.room_name = room_name
        self.room_type = room_type
        self.room_capacity = room_capacity
        self.room_occupants = room_occupants

    def __repr__(self):
        return "{}".format(self.room_name)


class Office(Room):
    """Class to create an Office and set it's attributes"""
    def __init__(self, room_name, room_type='office', room_capacity=6):
        super(Office, self).__init__(room_name, room_type, room_capacity)
        self.room_occupants = []

    def __repr__(self):
        return "{}".format(self.room_name)


class LivingSpace(Room):
    """Class to create a LivingSpace and set it's attributes"""
    def __init__(self, room_name, room_type='livingspace', room_capacity=4):
        super(LivingSpace, self).__init__(room_name, room_type, room_capacity)
        self.room_occupants = []

    def __repr__(self):
        return "{}".format(self.room_name)
