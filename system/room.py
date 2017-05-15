class Room(object):
    """Class to create a room object. Inherited by Office and LivingSpace"""

    def __init__(self, r_name=None, r_type=None, r_capacity=None, r_occupants=[]):
        self.r_name = r_name
        self.r_type = r_type
        self.r_capacity = r_capacity
        self.r_occupants = r_occupants

    def __repr__(self):
        return "{}".format(self.r_name)


class Office(Room):
    """Class to create an Office and set it's attributes"""
    def __init__(self, r_name, r_type='office', r_capacity=6):
        super(Office, self).__init__(r_name, r_type, r_capacity)
        self.r_occupants = []

    def __repr__(self):
        return "{}".format(self.r_name)


class LivingSpace(Room):
    """Class to create a LivingSpace and set it's attributes"""
    def __init__(self, r_name, r_type='livingspace', r_capacity=4):
        super(LivingSpace, self).__init__(r_name, r_type, r_capacity)
        self.r_occupants = []

    def __repr__(self):
        return "{}".format(self.r_name)
