import unittest
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from system.person import Person, Fellow, Staff


class PersonTestCases(unittest.TestCase):
    """
    Tests for the person class
    """
    def setUp(self):
        self.new_person = Person(person_name="Person", person_type="Random")
        self.new_fellow = Fellow("Faith Gori")
        self.new_staff = Staff("Robley Gori")

    def test_person_object(self):
        """
        Tests for the creation of a person and their attributes
        """
        self.assertTrue(self.new_person, "Person")
        self.assertEqual(self.new_person.person_name, "Person")
        self.assertEqual(self.new_person.person_type, "Random")
        self.assertTrue(isinstance(self.new_person.person_id, int))
        self.assertTrue(isinstance(self.new_person, Person))

    def test_staff_object(self):
        """
        Tests for the creation of a person and their attributes
        """
        self.assertTrue(self.new_staff, "Robley Gori")
        self.assertEqual(self.new_staff.person_name, "Robley Gori")
        self.assertEqual(self.new_staff.person_type, "staff")
        self.assertTrue(isinstance(self.new_staff.person_id, int))
        self.assertTrue(isinstance(self.new_staff, Staff))

    def test_fellow_object(self):
        """
        Tests for the creation of a person and their attributes
        """
        self.assertTrue(self.new_fellow, "Faith Gori")
        self.assertEqual(self.new_fellow.person_name, "Faith Gori")
        self.assertEqual(self.new_fellow.person_type, "fellow")
        self.assertTrue(isinstance(self.new_fellow.person_id, int))
        self.assertTrue(isinstance(self.new_fellow, Fellow))

if __name__ == "__main__":
    unittest.main()
