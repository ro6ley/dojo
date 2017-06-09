import unittest
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from system.person import Fellow, Staff


class PersonTestCases(unittest.TestCase):
    """
    Tests for the person class
    """
    def setUp(self):
        self.new_fellow = Fellow("Faith Gori")
        self.new_staff = Staff("Robley Gori")

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
