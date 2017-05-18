class Person(object):
    """Class to create a person object. Inherited by Fellow and Person"""
    def __init__(self, p_name=None, p_type=None):
        self.p_name = p_name
        self.p_type = p_type
        self.p_id = id(self)

    def __repr__(self):
        return "{}".format(self.p_name)


class Fellow(Person):
    """Class to create a Fellow and set their attributes"""
    def __init__(self, p_name, p_type="fellow"):
        super(Fellow, self).__init__(p_name, p_type)
        self.p_id = id(self)

    def __repr__(self):
        return "{}".format(self.p_name)


class Staff(Person):
    """Class to create a Staff and set their attributes"""
    def __init__(self, p_name, p_type="staff"):
        super(Staff, self).__init__(p_name, p_type)
        self.p_id = id(self)

    def __repr__(self):
        return "{}".format(self.p_name)
