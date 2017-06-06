class Person(object):
    """Class to create a person object. Inherited by Fellow and Person"""
    def __init__(self, person_name=None, person_type=None):
        self.person_name = person_name
        self.person_type = person_type
        self.person_id = id(self)

    def __repr__(self):
        return "{}".format(self.person_name)


class Fellow(Person):
    """Class to create a Fellow and set their attributes"""
    def __init__(self, person_name, person_type="fellow"):
        super(Fellow, self).__init__(person_name, person_type)
        self.person_id = id(self)

    def __repr__(self):
        return "{}".format(self.person_name)


class Staff(Person):
    """Class to create a Staff and set their attributes"""
    def __init__(self, person_name, person_type="staff"):
        super(Staff, self).__init__(person_name, person_type)
        self.person_id = id(self)

    def __repr__(self):
        return "{}".format(self.person_name)
