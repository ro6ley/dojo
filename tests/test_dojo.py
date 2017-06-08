import os
import sys
import unittest
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from system.person import Fellow, Staff
from system.room import Office, LivingSpace
from system.dojo import Dojo


class DojoTestCases(unittest.TestCase):
    """
    Tests for the Dojo class
    """

    def setUp(self):
        self.new_dojo = Dojo()
        self.new_dojo.create_room("Blue", "office")
        self.new_dojo.create_room("Mara", "livingspace")
        self.new_dojo.add_person("Another", "Lady", "fellow", True)
        self.new_dojo.add_person("Another", "Guy", "staff")

    def test_create_room(self):
        """
        Test the creation of a new office and livingspace
        """
        initial_office_count = len(self.new_dojo.rooms['offices'])
        office_yellow = self.new_dojo.create_room("Yellow", "office")
        self.assertIn(office_yellow, self.new_dojo.rooms['offices'])
        new_office_count = len(self.new_dojo.rooms['offices'])
        self.assertEqual(new_office_count - initial_office_count, 1)

        initial_livingspace_count = len(self.new_dojo.rooms["livingspaces"])
        livingspace_tsavo = self.new_dojo.create_room("Tsavo", "livingspace")
        self.assertIn(livingspace_tsavo, self.new_dojo.rooms["livingspaces"])
        new_livingspace_count = len(self.new_dojo.rooms["livingspaces"])
        self.assertEqual(new_livingspace_count - initial_livingspace_count, 1)

    def test_get_random_room(self):
        """
        Test that the function can return a room for allocation that has
        a vacant space
        """
        random_office = self.new_dojo.get_random_room("office")
        random_livingspace = self.new_dojo.get_random_room("livingspace")
        self.assertTrue(isinstance(random_office, Office))
        self.assertTrue(isinstance(random_livingspace, LivingSpace))

    def test_add_person(self):
        """
        Test the creation of a new fellow and staff
        """
        initial_fellow_count = len(self.new_dojo.people['fellows'])
        new_fellow = self.new_dojo.add_person("Robley", "Gori", "fellow", True)
        self.assertIn(new_fellow, self.new_dojo.people["fellows"])
        new_fellow_count = len(self.new_dojo.people['fellows'])
        self.assertEqual(new_fellow_count - initial_fellow_count, 1)

        initial_staff_count = len(self.new_dojo.people['staff'])
        new_staff = self.new_dojo.add_person("Faith", "Gori", "staff")
        self.assertIn(new_staff, self.new_dojo.people["staff"])
        new_staff_count = len(self.new_dojo.people['staff'])
        self.assertEqual(new_staff_count - initial_staff_count, 1)

    def test_print_allocations(self):
        """
        Test that allocations are printed on the screen
        and also output to file
        """
        # Data is entered
        self.new_dojo.add_person("Faith", "Gori", "staff")
        self.new_dojo.add_person("Robley", "Gori", "fellow", True)
        self.new_dojo.print_allocations("newfile.txt")
        file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..",
                            "output_files", "newfile.txt")
        # Check if file is created
        self.assertTrue(os.path.exists(file))

        with open(file) as myfile:
            lines = myfile.readlines()
            self.assertIn("Blue - office\n", lines)
            self.assertIn("Mara - livingspace\n", lines)
            self.assertIn("Faith Gori\n", lines)
            self.assertIn("Robley Gori\n", lines)
        os.remove(file)

    def test_load_people(self):
        """
        Test that people can be loaded from a text file and created
        The dictionary of people is supposed to be updated to include
        the new additions
        """
        self.new_dojo.load_people("test_load_people_file.txt")
        # People from file are added to application
        total_people = len(self.new_dojo.people['fellows']) + len(
            self.new_dojo.people['staff'])
        self.assertEqual(8, total_people)
        self.assertEqual(5, len(self.new_dojo.people['fellows']))
        self.assertEqual(3, len(self.new_dojo.people['staff']))

    def test_print_room(self):
        """
        Test that you can print the room members in a certain room.
        The function is supposed to return the allocations as a string.
        Also check if the room members appear in the list
        """
        self.new_dojo.add_person("Faith", "Gori", "staff")
        self.new_dojo.add_person("Robley", "Gori", "fellow", True)
        self.assertTrue(isinstance(self.new_dojo.print_room("Mara"), str))
        self.assertIn("Blue - office\n", self.new_dojo.print_room("Blue"))
        self.assertIn("Mara - livingspace\n", self.new_dojo.print_room("Mara"))
        self.assertIn("Faith Gori\n", self.new_dojo.print_room("Blue"))
        self.assertIn("Robley Gori\n", self.new_dojo.print_room("Mara"))

    def test_print_vacant_rooms(self):
        """
        Test that the function can return a list of rooms with vacancies
        """
        vacant_rooms = self.new_dojo.print_vacant_rooms()
        self.assertTrue(isinstance(vacant_rooms, list))

    def test_get_person_id(self):
        """
        Test that a user can get the id of a person or people with common names
        to use to reallocate them
        A list of the people matching the name is returned
        """
        # create the person
        self.new_dojo.add_person("Robley", "Gori", "staff")
        person_id = self.new_dojo.get_person_id("Robley Gori")
        self.assertTrue(isinstance(person_id, list))

    def test_get_person_object(self):
        """
        Test that you can find a user by their id and return them as an object
        for reallocation
        """
        # Add the person
        self.new_dojo.add_person("New", "Person", "fellow", True)
        self.new_dojo.add_person("New", "Lady", "staff")

        # Get their id
        new_staff = self.new_dojo.get_person_id("New Lady")[0]
        new_fellow = self.new_dojo.get_person_id("New Person")[0]

        # Use their id to get their object
        staff = self.new_dojo.get_person_object(new_staff.person_id)
        fellow = self.new_dojo.get_person_object(new_fellow.person_id)

        # Assert if the objects are instances of their respective classes
        self.assertTrue(isinstance(fellow, Fellow))
        self.assertTrue(isinstance(staff, Staff))

    def test_check_room(self):
        """
        Test that you can check if the room that the person is to be
        reallocated to exists and is available
        """
        self.new_dojo.create_room("Teal", "office")
        self.new_dojo.create_room("Kenya", "livingspace")
        office = self.new_dojo.check_room("Teal", "Robley Gori")
        livingspace = self.new_dojo.check_room("Kenya", "Robley Gori")
        no_office = self.new_dojo.check_room("Another", "Robley Gori")
        self.assertTrue(isinstance(office, Office))
        self.assertTrue(isinstance(livingspace, LivingSpace))
        self.assertFalse(no_office)

    def test_get_old_office(self):
        """
        Test that you can get a person old office before reallocating them to
        a new one
        """
        old_office = self.new_dojo.get_old_office("Another Lady")
        no_old_office = self.new_dojo.get_old_office("No Guy")
        self.assertTrue(isinstance(old_office, Office))
        self.assertFalse(no_old_office)

    def test_get_old_livingspace(self):
        """
        Test that you can get a person old living space before reallocating
        them to a new one
        """
        old_livingspace = self.new_dojo.get_old_livingspace("Another Lady")
        no_old_livingspace = self.new_dojo.get_old_livingspace("No Guy")
        self.assertTrue(isinstance(old_livingspace, LivingSpace))
        self.assertFalse(no_old_livingspace)

    def test_reallocate(self):
        """
        Test that you can reallocate a person to a new room
        """
        # create the person
        new_person = self.new_dojo.add_person("Robley", "Gori", "staff")
        # create a new empty room
        new_office = self.new_dojo.create_room("Yellow", "office")

        # check current room of the person
        for office in self.new_dojo.rooms['offices']:
            # Get the room in which the person is in
            if new_person in office.room_occupants:
                old_office = office

        # reallocate the person to new office
        self.new_dojo.reallocate_person(new_person.person_id,
                                        new_office.room_name)

        # Check if reallocation was successful
        new_office_location = self.new_dojo.rooms['offices'].index(new_office)
        new_office_members = self.new_dojo.rooms['offices'][
            new_office_location].room_occupants
        # Check if the person is in the new room
        self.assertIn(new_person, new_office_members)

    def test_print_unallocated(self):
        """
        Test that the program prints the unallocated individuals
        The function should also write the output to file
        """
        # Create isolated instance of the object that has no rooms created
        newDojo = Dojo()
        # Add new people, no rooms exist so they go to the unallocated list
        newDojo.add_person("New", "Guy", "staff")
        newDojo.add_person("New", "Lady", "fellow", False)
        newDojo.print_unallocated("newfile.txt")
        file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..",
                            "output_files", "newfile.txt")
        # Check if file is created
        self.assertTrue(os.path.exists(file))
        with open(file) as f:
            lines = f.readlines()
            self.assertIn("\tNew Guy - staff\n", lines)
            self.assertIn("\tNew Lady - fellow\n", lines)
        os.remove(file)

    def test_save_state(self):
        """
        Test that data can be saved from the system to the database
        """
        self.new_dojo.save_state("new_db.db")

        # database file existence
        self.assertTrue(os.path.exists("new_db.db"))
        os.remove("new_db.db")

    def test_load_state(self):
        """
        Test that data can be save to the database from the application
        Test that saved data can be loaded to the application from the database
        """
        # Save current data to database
        self.new_dojo.create_room("Hello", "office")
        self.new_dojo.save_state("test_dojo.db")

        # Check if database file is found
        self.assertTrue(os.path.exists("test_dojo.db"))

        # Get the database file and load it and check if our data was saved
        self.new_dojo.load_state("test_dojo.db")

        # Data is entered into the application
        total_rooms = len(self.new_dojo.rooms['offices']) + len(
            self.new_dojo.rooms['livingspaces'])
        total_people = len(self.new_dojo.people['fellows']) + len(
            self.new_dojo.people['staff'])

        # Assert that the number of people and rooms in database is
        # equal to the number that we created when setting up the class
        self.assertEqual(5, total_rooms)
        self.assertEqual(2, total_people)

        # Check if our created office was saved and retrieved
        loaded_offices = [office.room_name for office in
                          self.new_dojo.rooms["offices"]]
        self.assertIn("Hello", loaded_offices)

        # Check if the fellow we added was saved and retrieved
        loaded_people = [person.person_name for person in
                         self.new_dojo.people["fellows"]]
        self.assertIn("Another Lady", loaded_people)

        os.remove("test_dojo.db")

    def test_remove_person(self):
        """
        Test that a person can be removed from the dojo and any lists they may be in
        """
        new_fellow = self.new_dojo.add_person("Robley", "Gori", "fellow")
        new_staff = self.new_dojo.add_person("Faith", "Gori", "staff")

        initial_fellow_count = len(self.new_dojo.people["fellows"])
        initial_staff_count = len(self.new_dojo.people["staff"])
        # Remove the newly created people
        self.new_dojo.remove_person(new_fellow.person_id)
        self.new_dojo.remove_person(new_staff.person_id)

        new_fellow_count = len(self.new_dojo.people["fellows"])
        new_staff_count = len(self.new_dojo.people["staff"])

        self.assertEqual((initial_fellow_count - new_fellow_count), 1)
        self.assertEqual((initial_staff_count - new_staff_count), 1)

    def test_delete_room(self):
        """
        Test that a room can be deleted and all members sent to unallocated list
        """
        self.new_dojo.create_room("Teal", "office")
        self.new_dojo.create_room("Amboseli", "livingspace")
        initial_office_count = len(self.new_dojo.rooms["offices"])
        initial_livingspace_count = len(self.new_dojo.rooms["livingspaces"])
        self.new_dojo.delete_room("Teal")
        self.new_dojo.delete_room("Amboseli")

        new_office_count = len(self.new_dojo.rooms["offices"])
        new_livingsapce_count = len(self.new_dojo.rooms["livingspaces"])

        # Check if the number of rooms has reduced by one
        self.assertEqual((initial_office_count - new_office_count), 1)
        self.assertEqual((initial_livingspace_count - new_livingsapce_count), 1)

    def test_rename_room(self):
        """
        Test that a room can be renamed successfully
        """
        self.new_dojo.create_room("Teal", "office")
        self.new_dojo.create_room("Amboseli", "livingspace")

        self.new_dojo.rename_room("Teal", "Greeny")
        self.new_dojo.rename_room("Amboseli", "Ambo")

        self.assertIn("Ambo", [room.room_name for room in self.new_dojo.rooms["livingspaces"]])
        self.assertIn("Greeny", [room.room_name for room in self.new_dojo.rooms["offices"]])

        self.assertNotIn("Amboseli", [room.room_name for room in self.new_dojo.rooms["livingspaces"]])
        self.assertNotIn("Teal", [room.room_name for room in self.new_dojo.rooms["offices"]])

    def test_rename_person(self):
        """
        Test that a person's name can be edited
        """
        new_person = self.new_dojo.add_person("John", "Doe", "fellow")
        self.new_dojo.rename_person(new_person.person_id, "Johnn Doee")

        self.assertIn("Johnn Doee", [person.person_name for person in self.new_dojo.people["fellows"]])
        self.assertNotIn("John Doe", [person.person_name for person in self.new_dojo.people["fellows"]])


if __name__ == "__main__":
    unittest.main()
