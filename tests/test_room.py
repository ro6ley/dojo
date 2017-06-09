import unittest
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from system.room import Office, LivingSpace


class RoomTestCases(unittest.TestCase):
    """
    Tests for the creation of room objects and their attributes
    """
    def setUp(self):
        # set up the objects
        self.new_office = Office("Blue")
        self.new_livingspace = LivingSpace("Mara")

    def test_office_object(self):
        """
        Tests for the creation of an office and its attributes
        """
        self.assertTrue(self.new_office, "Blue")
        self.assertEqual(self.new_office.room_name, "Blue")
        self.assertTrue(self.new_office.room_type, "office")
        self.assertEqual(self.new_office.room_capacity, 6)
        self.assertEqual(self.new_office.room_occupants, [])
        self.assertTrue(isinstance(self.new_office, Office))

    def test_livingspace_object(self):
        """
        Tests for the creation of a living space and its attributes
        """
        self.assertTrue(self.new_livingspace, "Mara")
        self.assertEqual(self.new_livingspace.room_name, "Mara")
        self.assertTrue(self.new_livingspace.room_type, "livingspace")
        self.assertEqual(self.new_livingspace.room_capacity, 4)
        self.assertEqual(self.new_livingspace.room_occupants, [])
        self.assertTrue(isinstance(self.new_livingspace, LivingSpace))

if __name__ == "__main__":
    unittest.main()
