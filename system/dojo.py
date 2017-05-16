import sys
import os
import sqlite3
import random
from termcolor import cprint
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from system.person import Fellow, Staff
from system.room import Office, LivingSpace


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

    def add_person(self, f_name, l_name, p_type, wants_accommodation=False):
        """
        Method to create a fellow or staff, add them to the system and allocate
        them rooms
        """
        p_name = f_name + " " + l_name
        # if p_name in [f.p_name for f in self.people["fellows"]] or p_name in [s.p_name for s in self.people["staff"]]:
        #     print("Sorry. {} already exists in the system. Please try again".format(p_name))
        # else:
        if p_type == "fellow":
            new_fellow = Fellow(p_name)
            self.people["fellows"].append(new_fellow)
            cprint("Fellow {0} - id: {1} has been successfully added.".format(new_fellow.p_name, new_fellow.p_id), "green")

            if wants_accommodation is True:
                # Check if there is a vacant living space,
                # if none, add the fellow to the without living spaces list
                if [r for r in self.rooms["livingspaces"] if len(r.r_occupants) < r.r_capacity]:
                    fellow_livingspace = random.choice(
                        [r for r in self.rooms["livingspaces"] if len(r.r_occupants) < r.r_capacity])
                    fellow_livingspace.r_occupants.append(new_fellow)
                    self.people["with_livingspaces"].append(new_fellow)
                    cprint("{0} has been allocated the living space {1}.".format(f_name,
                                                                                fellow_livingspace.r_name), "green")
                else:
                    self.people["without_livingspaces"].append(new_fellow)
                    cprint(
                        "Sorry. No living space is currently available for {}. Please try again later".format(
                            new_fellow), "red")

            elif wants_accommodation is False:
                self.people["without_livingspaces"].append(new_fellow)

            # Check if there is a vacant office, if none, add the fellow to
            # the without offices list
            if [r for r in self.rooms["offices"] if len(r.r_occupants) < r.r_capacity]:
                fellow_office = random.choice(
                    [r for r in self.rooms["offices"] if len(r.r_occupants) < r.r_capacity])
                fellow_office.r_occupants.append(new_fellow)
                self.people["with_offices"].append(new_fellow)
                cprint("{0} has been allocated the office {1}.".format(f_name, fellow_office.r_name), "green")

            else:
                self.people["without_offices"].append(new_fellow)
                cprint(
                    "Sorry. No office is currently available for {}. Please try again later".format(new_fellow), "red")

            return new_fellow

        elif p_type == "staff":
            new_staff = Staff(p_name)
            self.people["staff"].append(new_staff)
            cprint("Staff {0} - id: {1} has been successfully added.".format(new_staff.p_name, new_staff.p_id), "green")

            # Check if there is a vacant office, if none, add the fellow to the
            # without offices list
            if [o for o in self.rooms["offices"] if len(o.r_occupants) < o.r_capacity]:
                staff_office = random.choice(
                    [o for o in self.rooms["offices"] if len(o.r_occupants) < o.r_capacity])
                staff_office.r_occupants.append(new_staff)
                self.people["with_offices"].append(new_staff)
                cprint("{0} has been allocated the office {1}.".format(f_name, staff_office.r_name), "green")

            else:
                self.people["without_offices"].append(new_staff)
                cprint(
                    "Sorry. No office is currently available for {}. Please try again later".format(new_staff), "red")

            return new_staff

    def create_room(self, r_name, r_type):
        """
        Method to create an office or living space as specified by the user
        """
        if r_type == "office":
            if r_name in [o.r_name for o in self.rooms["offices"]]:
                cprint("Sorry. Office {} already exists. \nPlease try again".format(r_name), "red")
            else:
                new_office = Office(r_name)
                self.rooms["offices"].append(new_office)
                cprint("An office called {} has been successfully created!".format(new_office.r_name), "green")
                return new_office

        elif r_type == "livingspace":
            if r_name in [ls.r_name for ls in self.rooms["livingspaces"]]:
                cprint("Sorry. The Living Space {} already exists.\nPlease try again".format(r_name), "red")
            else:
                new_livingspace = LivingSpace(r_name)
                self.rooms["livingspaces"].append(new_livingspace)
                cprint("A living space called {} has been successfully created!".format(new_livingspace.r_name), "green")
                return new_livingspace

    def print_allocations(self, filename=None):
        """
        Method to print room allocations to screen and optionally print the
        output to a text file
        """
        output = ""
        if self.rooms["offices"] or self.rooms["livingspaces"]:
            for office in self.rooms["offices"]:
                output += ("{0} - {1}\n".format(office.r_name, office.r_type))
                output += ("-" * 50) + "\n"
                if office.r_occupants:
                    for person in office.r_occupants:
                        output += (person.p_name + "\n")
                else:
                    output += "This room has no occupants.\n"
                output += "\n"

            for livingspace in self.rooms["livingspaces"]:
                output += ("{0} - {1}\n".format(livingspace.r_name, livingspace.r_type))
                output += ("-" * 50) + "\n"
                if livingspace.r_occupants:
                    for person in livingspace.r_occupants:
                        output += (person.p_name + "\n")
                else:
                    output += "This room has no occupants.\n"
                output += "\n"

            if filename:
                file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../output_files", filename)
                f = open(file, "w+")
                f.write(output)
                f.close()
                cprint("The allocations have been printed to the file - {}".format(filename), "yellow")

        else:
            output += "No rooms exist. Please create a room and try again\n"

        return output

    def print_unallocated(self, filename=None):
        """
        Method to print the list of unallocated members to the screen and
        optionally write the output to a text file
        """
        output = ""
        if self.people["without_livingspaces"]:
            output += "People without living spaces:\n"
            for person in self.people["without_livingspaces"]:
                output += " {0} - {1}\n".format(person.p_name, person.p_type)
        elif not self.people["without_livingspaces"]:
            output += "Every fellow has a living space in the Dojo.\n\n"

        if self.people["without_offices"]:
            output += "People without offices:\n"
            for person in self.people["without_offices"]:
                output += " {0} - {1}\n".format(person.p_name, person.p_type)
        elif not self.people["without_offices"]:
            output += "Everyone has an office in the Dojo.\n"

        if filename:
            file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../output_files", filename)
            f = open(file, "w+")
            f.write(output)
            f.close()
            cprint("The allocations have been printed to the file - {}".format(filename), "yellow")

        return output

    def print_room(self, r_name):
        """
        Method to print the members of a single room to the screen
        """
        rooms = self.rooms["offices"] + self.rooms["livingspaces"]
        output = ""
        if r_name not in [r.r_name for r in rooms]:
            return "Sorry. The room you have entered does not exist. Please try again"
        for r in rooms:
            if r.r_name == r_name:
                output += ("{0} - {1}\n".format(r.r_name, r.r_type))
                output += ("-" * 50) + "\n"
                if r.r_occupants:
                    for p in r.r_occupants:
                        output += (p.p_name + "\n")
                else:
                    output += "This room has no occupants.\n"
        return output

    def get_person_id(self, p_name):
        """
        This method will get a person's unique ID given their names to help the
        user in reallocating a person
        """
        fellows = []
        staff = []
        if p_name in [p.p_name for p in self.people["fellows"]]:
            for person in self.people["fellows"]:
                if person.p_name == p_name:
                    fellows.append(person)
            for f in fellows:
                cprint("Fellow {0} - id: {1}".format(f.p_name, f.p_id), "green")

            return fellows

        if p_name in [p.p_name for p in self.people["staff"]]:
            for person in self.people["staff"]:
                if person.p_name == p_name:
                    staff.append(person)
            for f in staff:
                cprint("Staff {0} - id: {1}".format(f.p_name, f.p_id), "green")

            return staff

        elif p_name not in [p.p_name for p in self.people["fellows"]] or p_name not in [p.p_name for p in self.people["staff"]]:
            cprint("{} does not exist in the system. Please add them first to get their id.".format(p_name), "red")
            person_id = 0
            return person_id

    def get_person_object(self, p_id):
        """
        Method to check if a person exists before reallocation
        """
        all_people = self.people["fellows"] + self.people["staff"]
        if p_id in [p.p_id for p in all_people]:
            for p in all_people:
                if p.p_id == p_id:
                    return p

        elif p_id not in [f.p_id for f in all_people]:
            return None

    def check_room(self, r_name, p_name):
        """
        Method to check if the room that the person is to be reallocated to exists,
        is vacant and the person is not already in it.
        """
        all_rooms = self.rooms["offices"] + self.rooms["livingspaces"]
        if r_name in [r.r_name for r in all_rooms]:
            for r in all_rooms:
                if r.r_name == r_name and len(r.r_occupants) < r.r_capacity and p_name not in [p.p_name for p in r.r_occupants]:
                    return r
                elif r.r_name == r_name and len(r.r_occupants) >= r.r_capacity:
                    return "full"
                elif r.r_name == r_name and p_name in [p.p_name for p in r.r_occupants]:
                    return "present"

        elif r_name not in [r.r_name for r in all_rooms]:
            return None

    def get_old_office(self, p_name):
        """
        Method to get the previous office that the person is in
        """
        for room in self.rooms["offices"]:
            if p_name in [p.p_name for p in room.r_occupants]:
                return room

    def get_old_livingspace(self, p_name):
        """
        Method to get the previous living space that the person is in
        """
        for room in self.rooms["livingspaces"]:
            if p_name in [p.p_name for p in room.r_occupants]:
                return room

    def reallocate_person(self, p_id, r_name):
        """
        Method to reallocate an individual from one room to another using their names
        """
        new_person = self.get_person_object(p_id)
        if new_person is not None:
            new_room = self.check_room(r_name, new_person.p_name)
            old_office = self.get_old_office(new_person.p_name)
            old_livingspace = self.get_old_livingspace(new_person.p_name)

            if isinstance(new_person, Fellow) or isinstance(new_person, Staff):
                if new_room != "full" and new_room != "present" and new_room:
                    if isinstance(new_room, LivingSpace):
                        if isinstance(new_person, Staff):
                            cprint("Cannot reallocate staff to a living space", "red")
                        elif isinstance(new_person, Fellow):
                            if isinstance(old_livingspace, LivingSpace) and new_person in old_livingspace.r_occupants:
                                new_room.r_occupants.append(
                                    old_livingspace.r_occupants.pop(old_livingspace.r_occupants.index(new_person)))
                                cprint("{0} has been reallocated to {1} from {2}".format(new_person.p_name, r_name,
                                                                                        old_livingspace.r_name), "green")
                            elif new_person in self.people["without_livingspaces"]:
                                self.people["without_livingspaces"].remove(new_person)
                                new_room.r_occupants.append(new_person)
                                cprint("{0} has been reallocated to {1} from unallocated".format(new_person.p_name, r_name), "green")
                            else:
                                cprint("{} has not been reallocated.".format(new_person.p_name), "green")

                    elif isinstance(new_room, Office):
                        if isinstance(old_office, Office) and new_person in old_office.r_occupants:
                            new_room.r_occupants.append(
                                old_office.r_occupants.pop(old_office.r_occupants.index(new_person)))
                            cprint("{0} has been reallocated to {1} from {2}".format(new_person.p_name, r_name, old_office.r_name), "green")
                        elif new_person in self.people["without_offices"]:
                            self.people["without_offices"].remove(new_person)
                            new_room.r_occupants.append(new_person)
                            cprint("{0} has been reallocated to {1}".format(new_person.p_name, r_name), "green")
                        else:
                            cprint("{} has not been reallocated.".format(new_person.p_name), "red")

                elif new_room == "full":
                    cprint("Sorry. {} is already full".format(r_name), "red")

                elif new_room == "present":
                    cprint("Sorry. {0} is already in room {1}".format(new_person.p_name, r_name), "red")

                elif new_room is None:
                    cprint("Sorry. Room {} doest not exist in the system.".format(r_name), "red")

        elif new_person is None:
            cprint("Sorry. {} does not exist in the system. Please try again later".format(p_id), "red")

        else:
            cprint("We ran into an error", "red")

        return self.rooms

    def load_people(self, filename="input.txt"):
        """
        Method to load people from text file and allocate them rooms
        """
        file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../input_files", filename)
        if file:
            f = open(file, "r")
            for line in f:
                f_name = line.split()[0]
                l_name = line.split()[1]
                p_name = f_name + " " + l_name
                person_type = line.split()[2]
                if len(line.split()) == 4 and person_type == "FELLOW":
                    self.add_person(f_name, l_name, p_type="fellow", wants_accommodation=True)
                    print("")

                elif len(line.split()) == 3 and person_type == "FELLOW":
                    self.add_person(f_name, l_name, p_type="fellow")
                    print("")

                elif len(line.split()) == 3 and person_type == "STAFF":
                    self.add_person(f_name, l_name, p_type="staff")
                    print("")
        else:
            cprint("The filename you provided does not exist or is empty. Please check and try again.", "red")

    def save_state(self, db_name="dojo.db"):
        """Method to save details to db using SQL"""
        # Create database
        # Create tables: fellows, staff, without_offices, without_livingspaces, offices, livingspaces
        # Fellow/Staff structure: id, first name, last name, type
        # Office/Livingspace structure: id, room name, room type, room_members_ids
        pass

    def load_state(self, db_name="dojo.db"):
        """Method to load the data stored in the database"""
        # Open db if exists
        # Read tables
        # Add people to system
        # Add rooms while recreating the people objects and saving them to their rooms
        pass
