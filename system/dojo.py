import sys
import os
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from termcolor import cprint
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from system.person import Fellow, Staff
from system.room import Office, LivingSpace
from system.models import People, Rooms, Unallocated, BASE

BASE_DIR = ""


class Dojo(object):
    """
    Main dojo class that manages the system and the data
    """
    def __init__(self):
        self.people = {
            "fellows": [],
            "staff": [],
            "with_offices": [],
            "without_offices": [],
            "with_livingspaces": [],
            "without_livingspaces": []
        }
        self.rooms = {
            "offices": [],
            "livingspaces": []
        }

    def get_random_room(self, room_type):
        """
        Method to return an office or living space that has a vacancy
        """
        # Get a random office
        if room_type == "office":
            if [room for room in self.rooms["offices"]
               if len(room.room_occupants) < room.room_capacity]:
                random_office = random.choice(
                    [room for room in self.rooms["offices"] if
                     len(room.room_occupants) < room.room_capacity])

                return random_office

        # Get a random living space
        elif room_type == "livingspace":
            if [room for room in self.rooms["livingspaces"]
               if len(room.room_occupants) < room.room_capacity]:
                random_livingspace = random.choice(
                    [room for room in self.rooms["livingspaces"] if
                     len(room.room_occupants) < room.room_capacity])

                return random_livingspace

    def add_person(self, first_name, last_name,
                   person_type, wants_accommodation=False):
        """
        Method to create a fellow or staff, add them to the system and allocate
        them rooms
        """
        person_name = first_name + " " + last_name
        if person_type == "fellow":
            new_fellow = Fellow(person_name)
            self.people["fellows"].append(new_fellow)
            cprint("Fellow {0} - id: {1} has been successfully added.".format(
                new_fellow.person_name, new_fellow.person_id), "green")

            if wants_accommodation is True:
                # Check if there is a vacant living space,
                # if none, add the fellow to the without living spaces list
                fellow_livingspace = self.get_random_room("livingspace")
                if fellow_livingspace is not None:
                    fellow_livingspace.room_occupants.append(new_fellow)
                    self.people["with_livingspaces"].append(new_fellow)
                    cprint(
                        "{0} has been allocated the living space {1}.".format(
                            first_name,
                            fellow_livingspace.room_name), "green")
                else:
                    self.people["without_livingspaces"].append(new_fellow)
                    cprint("Sorry."
                           "No living space is currently available for {}."
                           "Please try again later".format(new_fellow), "red")

            elif wants_accommodation is False:
                self.people["without_livingspaces"].append(new_fellow)

            # Check if there is a vacant office, if none, add the fellow to
            # the without offices list
            fellow_office = self.get_random_room("office")
            if fellow_office is not None:
                fellow_office.room_occupants.append(new_fellow)
                self.people["with_offices"].append(new_fellow)
                cprint("{0} has been allocated the office {1}."
                       .format(first_name, fellow_office.room_name), "green")

            else:
                self.people["without_offices"].append(new_fellow)
                cprint("Sorry. No office is currently available for {}."
                       "Please try again later".format(new_fellow), "red")

            return new_fellow

        elif person_type == "staff":
            new_staff = Staff(person_name)
            self.people["staff"].append(new_staff)
            cprint("Staff {0} - id: {1} has been successfully added.".format(
                new_staff.person_name, new_staff.person_id), "green")

            # Check if there is a vacant office, if none, add the fellow to the
            # without offices list
            staff_office = self.get_random_room("office")
            if staff_office is not None:
                staff_office.room_occupants.append(new_staff)
                self.people["with_offices"].append(new_staff)
                cprint("{0} has been allocated the office {1}.".
                       format(first_name, staff_office.room_name), "green")
            else:
                self.people["without_offices"].append(new_staff)
                cprint("Sorry. No office is currently available for {}."
                       "Please try again later".format(new_staff), "red")

            return new_staff

    def create_room(self, room_name, room_type):
        """
        Method to create an office or living space as specified by the user
        """
        all_rooms = self.rooms["offices"] + self.rooms["livingspaces"]
        if room_type == "office":
            if room_name in [office.room_name for office in all_rooms]:
                cprint(
                    "Sorry. A room called {} already exists. Please try again"
                    .format(room_name), "red")
            else:
                new_office = Office(room_name)
                self.rooms["offices"].append(new_office)
                cprint("An office called {} has been successfully created!"
                       .format(new_office.room_name), "green")
                return new_office

        elif room_type == "livingspace":
            if room_name in [livingspace.room_name for livingspace in
                             all_rooms]:
                cprint("Sorry. A room called {} already exists. "
                       "Please try again".format(room_name), "red")
            else:
                new_livingspace = LivingSpace(room_name)
                self.rooms["livingspaces"].append(new_livingspace)
                cprint("A living space called {} has been successfully created"
                       .format(new_livingspace.room_name), "green")
                return new_livingspace

    def print_allocations(self, filename=None):
        """
        Method to print room allocations to screen and optionally print the
        output to a text file
        """
        output = ""
        if self.rooms["offices"] or self.rooms["livingspaces"]:
            for office in self.rooms["offices"]:
                cprint("\n" + ("-" * 50), "green")
                cprint("{0} - {1}".format(office.room_name, office.room_type),
                       "green")
                cprint(("-" * 50), "green")
                output += ("{0} - {1}\n".format(office.room_name,
                                                office.room_type))
                output += ("-" * 50) + "\n"
                if office.room_occupants:
                    for person in office.room_occupants:
                        cprint(person.person_name, "green")
                        output += (person.person_name + "\n")
                else:
                    cprint("This room has no occupants.\n", "red")
                    output += "This room has no occupants.\n"
                output += "\n"

            for livingspace in self.rooms["livingspaces"]:
                cprint("\n" + ("-" * 50), "green")
                cprint("{0} - {1}".format(livingspace.room_name,
                                          livingspace.room_type), "green")
                cprint(("-" * 50), "green")
                output += (
                    "{0} - {1}\n".format(livingspace.room_name,
                                         livingspace.room_type))
                output += ("-" * 50) + "\n"
                if livingspace.room_occupants:
                    for person in livingspace.room_occupants:
                        cprint(person.person_name, "green")
                        output += (person.person_name + "\n")
                else:
                    cprint("This room has no occupants.", "red")
                    output += "This room has no occupants.\n"
                output += "\n"

            if filename:
                file = os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "..", "output_files", filename)
                output_file = open(file, "w+")
                output_file.write(output)
                output_file.close()
                cprint("The allocations have been printed to the file - {}".
                       format(filename), "yellow")

        else:
            cprint("No rooms exist. Please create a room and try again\n",
                   "red")
            output += "No rooms exist. Please create a room and try again\n"

        return output

    def print_unallocated(self, filename=None):
        """
        Method to print the list of unallocated members to the screen and
        optionally write the output to a text file
        """
        output = ""
        if self.people["without_livingspaces"]:
            cprint("People without living spaces:\n", "yellow")
            output += "People without living spaces:\n"
            for person in self.people["without_livingspaces"]:
                cprint("\t{0} - {1}".format(person.person_name,
                                            person.person_type), "yellow")
                print("")
                output += "\t{0} - {1}\n".format(person.person_name,
                                                 person.person_type)
        elif not self.people["without_livingspaces"] and self.people["fellows"]:
            cprint("Every fellow has a living space in the Dojo.\n", "green")
            output += "Every fellow has a living space in the Dojo.\n\n"

        if self.people["without_offices"]:
            cprint("People without offices:\n", "yellow")
            output += "People without offices:\n"
            for person in self.people["without_offices"]:
                cprint("\t{0} - {1}".format(person.person_name,
                                            person.person_type), "yellow")
                print("")
                output += "\t{0} - {1}\n".format(person.person_name,
                                                 person.person_type)
        elif not self.people["without_offices"] and self.people["fellows"] or\
                self.people["staff"]:
            cprint("Everyone has an office in the Dojo.\n", "green")
            output += "Everyone has an office in the Dojo.\n"

        else:
            cprint("There are no people in the Dojo currently.", "red")

        if filename:
            file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                "..", "output_files", filename)
            output_file = open(file, "w+")
            output_file.write(output)
            output_file.close()
            cprint("The allocations have been printed to the file - {}".format(
                filename), "yellow")

        return output

    def print_room(self, room_name):
        """
        Method to print the members of a single room to the screen
        """
        rooms = self.rooms["offices"] + self.rooms["livingspaces"]
        output = ""
        if room_name not in [room.room_name for room in rooms]:
            cprint("Sorry. The room you have entered does not exist."
                   "Please try again", "red")
            return "Sorry. The room you have entered does not exist. \
                                                        Please try again"
        for room in rooms:
            if room.room_name == room_name:
                cprint(("{0} - {1}".format(room.room_name, room.room_type)),
                       "green")
                cprint(("-" * 50), "green")
                output += (
                    "{0} - {1}\n".format(room.room_name, room.room_type))
                output += ("-" * 50) + "\n"
                if room.room_occupants:
                    for person in room.room_occupants:
                        cprint(person.person_name, "green")
                        output += (person.person_name + "\n")
                else:
                    cprint("This room has no occupants.", "red")
                    output += "This room has no occupants.\n"
        return output

    def print_vacant_rooms(self):
        """
        Method to print all rooms in the Dojo that have vacant spaces
        """
        all_rooms = self.rooms["offices"] + self.rooms["livingspaces"]
        if all_rooms:
            vacant_rooms = [room for room in all_rooms if
                            len(room.room_occupants) < room.room_capacity]
            if vacant_rooms is not None:
                for room in vacant_rooms:
                    empty_spaces = room.room_capacity - len(
                        room.room_occupants)
                    cprint("\t{0} - Vacant spaces {1}".format(
                        room.room_name, empty_spaces), "green")
                return vacant_rooms

            elif vacant_rooms is None:
                cprint("\tSorry there are no vacant rooms at the moment.",
                       "red")
                return []
        else:
            cprint("\tSorry there are no vacant rooms  at the moment.", "red")
            return []

    def get_person_id(self, person_name):
        """
        This method will get a person's unique ID given their names to help the
        user in reallocating a person
        """
        fellows = []
        staff = []
        if person_name in [person.person_name for person in
                           self.people["fellows"]]:
            for person in self.people["fellows"]:
                if person.person_name == person_name:
                    fellows.append(person)
            for fellow in fellows:
                cprint("Fellow {0} - id: {1}".format(
                    fellow.person_name, fellow.person_id), "green")

            return fellows

        if person_name in [p.person_name for p in self.people["staff"]]:
            for person in self.people["staff"]:
                if person.person_name == person_name:
                    staff.append(person)
            for f in staff:
                cprint("Staff {0} - id: {1}".format(
                    f.person_name, f.person_id), "green")

            return staff

        elif person_name not in [p.person_name for p in
                                 self.people["fellows"]] or person_name not in\
                [p.person_name for p in self.people["staff"]]:
            cprint("{} does not exist in the system. \
                Please add them first to get their id.".format(person_name),
                   "red")
            person_id = 0
            return person_id

    def get_person_object(self, person_id):
        """
        Method to check if a person exists before reallocation
        """
        all_people = self.people["fellows"] + self.people["staff"]
        if person_id in [person.person_id for person in all_people]:
            for person in all_people:
                if person.person_id == person_id:
                    return person

        elif person_id not in [person.person_id for person in all_people]:
            return None

    def check_room(self, room_name, person_id):
        """
        Method to check if the room that the person is to be reallocated to
        exists, is vacant and the person is not already in it.
        """
        all_rooms = self.rooms["offices"] + self.rooms["livingspaces"]
        if room_name in [room.room_name for room in all_rooms]:
            for room in all_rooms:
                if room.room_name == room_name and len(room.room_occupants) < \
                        room.room_capacity and person_id not in \
                        [person.person_id for person in room.room_occupants]:
                    return room
                elif room.room_name == room_name and len(room.room_occupants) \
                        >= room.room_capacity:
                    return "full"
                elif room.room_name == room_name and person_id in \
                        [person.person_id for person in room.room_occupants]:
                    return "present"

        elif room_name not in [room.room_name for room in all_rooms]:
            return None

    def get_old_office(self, person_id):
        """
        Method to get the previous office that the person is in
        """
        for room in self.rooms["offices"]:
            if person_id in [person.person_id for
                               person in room.room_occupants]:
                return room

    def get_old_livingspace(self, person_id):
        """
        Method to get the previous living space that the person is in
        """
        for room in self.rooms["livingspaces"]:
            if person_id in [person.person_id for
                               person in room.room_occupants]:
                return room

    def allocate_person(self, person_id, room_type):
        """
        Method to allocate a person to an available room randomly
        """
        person = self.get_person_object(person_id)
        if person:
            if room_type is "livingspace":
                if person in self.people["without_livingspaces"]:
                    livingspace = self.get_random_room("livingspace")
                    if livingspace is not None:
                        livingspace.room_occupants.append(person)
                        self.people["without_livingspaces"].remove(person)
                        self.people["with_livingspaces"].append(person)
                        cprint(
                            "{0} has been allocated the living space {1}.".format(
                                person.person_name, livingspace.room_name),
                            "green")
                    else:
                        cprint("Sorry."
                               "No living space is currently available for {}."
                               "Please try again later".format(
                            person.person_name),
                               "red")
                else:
                    cprint("Sorry. {} already has a livingspace. Reallocate "
                           "them instead".format(person.person_name), "red")

            elif room_type is "office":
                if person in self.people["without_offices"]:
                    office = self.get_random_room("office")
                    if office is not None:
                        office.room_occupants.append(person)
                        self.people["without_offices"].remove(person)
                        self.people["with_offices"].append(person)
                        cprint(
                            "{0} has been allocated the living space {1}.".format(
                                person.person_name, office.room_name), "green")
                    else:
                        cprint("Sorry."
                               "No living space is currently available for {}."
                               "Please try again later".format(
                            person.person_name),
                               "red")
                else:
                    cprint("Sorry. {} already has an office. Reallocate "
                           "them instead".format(person.person_name), "red")

        elif person is None:
            cprint("Error. {} cannot be found in the system. Check and try"
                   " again".format(person_id), "red")

    def reallocate_person(self, person_id, room_name):
        """
        Method to reallocate an individual from one room to another using their
        ids
        """
        new_person = self.get_person_object(person_id)
        if new_person is not None:
            new_room = self.check_room(room_name, new_person.person_id)
            old_office = self.get_old_office(new_person.person_id)
            old_livingspace = self.get_old_livingspace(new_person.person_id)

            if isinstance(new_person, Fellow) or isinstance(new_person, Staff):
                if new_room is not "full" and new_room is not "present" and \
                        new_room:
                    if isinstance(new_room, LivingSpace):
                        if isinstance(new_person, Staff):
                            cprint("Cannot reallocate staff to a living space",
                                   "red")
                        elif isinstance(new_person, Fellow):
                            if isinstance(old_livingspace, LivingSpace) and \
                                            new_person in \
                                            old_livingspace.room_occupants:
                                new_room.room_occupants.append(
                                    old_livingspace.room_occupants.pop(
                                        old_livingspace.room_occupants.index(
                                            new_person)))
                                cprint("{0} has been reallocated "
                                       "to {1} from {2}".format(
                                        new_person.person_name, room_name,
                                        old_livingspace.room_name), "green")
                            elif new_person in \
                                    self.people["without_livingspaces"]:
                                cprint("{0} cannot be reallocated. "
                                       "Allocate them a room first".format(
                                        new_person.person_name), "red")
                            else:
                                cprint("{} has not been reallocated.".format(
                                    new_person.person_name), "green")

                    elif isinstance(new_room, Office):
                        if isinstance(old_office, Office) and \
                                       new_person in old_office.room_occupants:
                            new_room.room_occupants.append(
                                old_office.room_occupants.pop(
                                    old_office.room_occupants.index(
                                        new_person)))
                            cprint("{0} has been reallocated to {1} from {2}".
                                   format(new_person.person_name, room_name,
                                          old_office.room_name), "green")
                        elif new_person in self.people["without_offices"]:
                            cprint("{0} cannot be reallocated. "
                                   "Allocate them a room first".format(
                                        new_person.person_name), "red")
                        else:
                            cprint("{} has not been reallocated.".format(
                                new_person.person_name), "red")

                elif new_room is "full":
                    cprint("Sorry. {} is already full".format(room_name),
                           "red")

                elif new_room is "present":
                    cprint("Sorry. {0} is already in room {1}".format(
                        new_person.person_name, room_name), "red")

                elif new_room is None:
                    cprint(
                        "Sorry. Room {} doest not exist in the system.".format(
                            room_name), "red")

        elif new_person is None:
            cprint("Sorry. {} does not exist in the system. \
                   Please try again later".format(person_id), "red")

        else:
            cprint("We ran into an error", "red")

        return self.rooms

    def load_people(self, filename="input.txt"):
        """
        Method to load people from text file and allocate them rooms
        """
        file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                            "..", "input_files", filename)
        try:
            input_file = open(file, "r")
            # Will return None if file is empty
            content = input_file.read(1)
            if input_file and content:
                for line in input_file:
                    first_name = line.split()[0]
                    last_name = line.split()[1]
                    person_name = first_name + " " + last_name
                    person_type = line.split()[2]
                    if len(line.split()) == 4 and person_type == "FELLOW":
                        self.add_person(first_name, last_name,
                                        person_type="fellow",
                                        wants_accommodation=True)
                        print("")

                    elif len(line.split()) == 3 and person_type == "FELLOW":
                        self.add_person(first_name, last_name,
                                        person_type="fellow")
                        print("")

                    elif len(line.split()) == 3 and person_type == "STAFF":
                        self.add_person(first_name, last_name,
                                        person_type="staff")
                        print("")
            else:
                cprint("The file you provided is empty."
                       "Please check and try again.", "red")

        except FileNotFoundError:
            cprint("\tThe file {} was not found. Check and try again"
                   .format(filename), "red")

    def save_state(self, db_name="dojo.db"):
        """Method to save details to db using SQL"""
        # Create database
        if os.path.exists(db_name):
            os.remove(db_name)

        engine = create_engine("sqlite:///{}".format(db_name))
        BASE.metadata.bind = engine
        BASE.metadata.create_all(engine)
        cprint("Database created", "green")

        Session = sessionmaker(bind=engine)
        session = Session()

        all_people = self.people["staff"] + self.people["fellows"]
        if all_people:
            cprint("\tSaving the people in the dojo...", "green")
            for person in all_people:
                new_person = People(
                    person.person_id, person.person_name, person.person_type
                )
                session.add(new_person)
                session.commit()
            cprint("\tDone.", "green")
        else:
            cprint("\tThere are no people in the Dojo to be saved.", "yellow")

        all_rooms = self.rooms["offices"] + self.rooms["livingspaces"]
        if all_rooms:
            cprint("\tSaving the rooms in the dojo...", "green")
            for room in all_rooms:
                room_occupants = ",".join([str(person.person_id) for person
                                           in room.room_occupants])
                new_room = Rooms(
                    room.room_name, room.room_type, room.room_capacity,
                    room_occupants)
                session.add(new_room)
                session.commit()
            cprint("\tDone.", "green")
        else:
            cprint("There are no rooms in the Dojo to be saved", "yellow")

        all_unallocated = self.people["without_offices"] + \
            self.people["without_livingspaces"]
        if all_unallocated:
            cprint("\tSaving the unallocated people in the dojo...", "green")
            for person in self.people["without_offices"]:
                new_unallocated = Unallocated(
                    person.person_id, person.person_name, person.person_type,
                    without_room="office")

                session.add(new_unallocated)
                session.commit()

            for person in self.people["without_livingspaces"]:
                new_unallocated = Unallocated(
                    person.person_id, person.person_name, person.person_type,
                    without_room="livingspace"
                )
                session.add(new_unallocated)
                session.commit()

            cprint("\tDone.", "green")

        else:
            cprint("There are no people who are unallocated \
            in the dojo to be saved.", "yellow")

    def load_state(self, db_name="dojo.db"):
        """Method to load the data stored in the database"""
        # Open db if exists
        if os.path.exists(db_name):
            engine = create_engine("sqlite:///{}".format(db_name))

            # Create a session
            Session = sessionmaker(bind=engine)
            session = Session()

            # Get people
            if session.query(People):
                cprint("\tLoading people from the database...", "green")
                for person in session.query(People):
                    if person.person_type == "fellow":
                        # Recreate the fellow
                        old_fellow = Fellow(person.names, person_type="fellow")
                        old_fellow.person_id = person.person_id
                        self.people["fellows"].append(old_fellow)
                    elif person.person_type == "staff":
                        # Recreate the staff
                        old_staff = Staff(person.names, person_type="staff")
                        old_staff.person_id = person.person_id
                        self.people["staff"].append(old_staff)

                cprint("\tAll the people have been loaded from the database",
                       "green")
            else:
                cprint("\tNo people in the database", "red")

            # Get rooms
            if session.query(Rooms):
                cprint("\tLoading rooms from the database...", "green")
                for room in session.query(Rooms):
                    if room.room_type == "office":
                        # Create the offices
                        old_office = Office(room.room_name,
                                            room_capacity=room.room_capacity)
                        # Use the ids to populate the occupants from people
                        members = [int(person_id) for person_id in
                                   room.room_occupants.split(",") if person_id]
                        if len(members) > 0:
                            for member in members:
                                old_office.room_occupants.append(
                                    self.get_person_object(member))

                            self.rooms["offices"].append(old_office)

                    elif room.room_type == "livingspace":
                        # Create the offices
                        old_livingspace = LivingSpace(
                            room.room_name, room_capacity=room.room_capacity)
                        # Use the ids to populate the occupants from people
                        members = [int(person_id) for person_id in
                                   room.room_occupants.split(",") if person_id]
                        if len(members) > 0:
                            for member in members:
                                old_livingspace.room_occupants.append(
                                    self.get_person_object(member))

                        self.rooms["livingspaces"].append(old_livingspace)

                cprint("\tAll the rooms have been loaded from the database",
                       "green")

            else:
                cprint("\tNo rooms in the database", "red")

            # Get unallocated
            if session.query(Unallocated):
                cprint("\tUpdating list of unallocated people...", "green")
                for person in session.query(Unallocated):
                    if person.without_room == "office":
                        self.people["without_offices"].append(
                            self.get_person_object(person.person_id))
                    elif person.without_room == "livingspace":
                        self.people["without_livingspaces"].append(
                            self.get_person_object(person.person_id))

                cprint("\tList of unallocated people has been updated",
                       "green")
            else:
                cprint("\tThere are no unallocated people in the database",
                       "green")
        else:
            cprint("\tThe database {} does not exist.".format(db_name), "red")

    def delete_room(self, room_name):
        """
        Method to delete a room from the system and add members
        to list of unallocated
        """
        all_rooms = self.rooms["offices"] + self.rooms["livingspaces"]
        if room_name in [room.room_name for room in all_rooms]:
            for room in all_rooms:
                if room.room_name == room_name and room.room_type == "office":
                    for member in room.room_occupants:
                        self.people["without_offices"].append(member)
                    self.rooms["offices"].pop(
                        self.rooms["offices"].index(room))
                    cprint("The office {} has been deleted successfully. All"
                           "members have been added to the list of unallocated"
                           "members".format(room_name), "green")
                elif room.room_name == room_name and \
                        room.room_type == "livingspace":
                    for member in room.room_occupants:
                        self.people["without_livingspaces"].append(member)
                    self.rooms["livingspaces"].pop(
                        self.rooms["livingspaces"].index(room))
                    cprint("The livingspace {} has been deleted successfully."
                           "All members have been added to the list of "
                           "unallocated members".format(room_name), "green")

        else:
            cprint("Sorry. That room does not exist. Please try again.", "red")

    def remove_person(self, person_id):
        """
        Method to remove a person from the system
        """
        person = self.get_person_object(int(person_id))
        if person:
            if person in self.people["without_livingspaces"]:
                self.people["without_livingspaces"].pop(
                    self.people["without_livingspaces"].index(person))
                cprint("{} has been removed from the unallocated list"
                       .format(person.person_name), "green")
            elif person in self.people["without_offices"]:
                self.people["without_offices"].pop(
                    self.people["without_offices"].index(person))
                cprint("{} has been removed from the unallocated list".
                       format(person.person_name), "green")
            all_rooms = self.rooms["offices"] + self.rooms["livingspaces"]
            for room in all_rooms:
                if person in room.room_occupants:
                    room.room_occupants.pop(room.room_occupants.index(person))
                    cprint("{0} has been removed from {1}".format(
                        person.person_name, room.room_name), "green")

            if person in self.people["fellows"]:
                self.people["fellows"].pop(
                    self.people["fellows"].index(person))
                cprint("{} has been successfully removed from the Dojo".
                       format(person.person_name), "green")
            elif person in self.people["staff"]:
                self.people["staff"].pop(self.people["staff"].index(person))
                cprint("{} has been successfully removed from the Dojo".
                       format(person.person_name), "green")
        else:
            cprint("Sorry. The person with id: {} could not be found."
                   "Please check and try again".format(person_id), "red")

    def rename_room(self, room_name, new_room_name):
        """
        Method to change the name of a room in the system
        """
        all_rooms = self.rooms["offices"] + self.rooms["livingspaces"]
        if room_name in [room.room_name for room in all_rooms]:
            for room in all_rooms:
                if room.room_name == room_name:
                    room.room_name = new_room_name
                    cprint("{0} has been successfully renamed to {1}".
                           format(room_name, new_room_name))
        else:
            cprint("Sorry. {} could not be found. Try again".format(room_name),
                   "red")

    def rename_person(self, person_id, new_names):
        """
        Method to change the name of a person in the system
        """
        person = self.get_person_object(int(person_id))
        if person:
            old_person_name = person.person_name
            person.person_name = new_names
            cprint("{0}'s name has been changed to {1}".
                   format(old_person_name, new_names), "green")
        else:
            cprint("Sorry. The person with id: {} could not be found."
                   "Please check and try again".format(person_id), "red")
