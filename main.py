#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    ██████ █    █ █████       ███▄▄  ████▄ ██████ ████▄
      ██   █▄▄▄▄█ █▄▄▄▄       █    █ █   █   ██   █   █
      ██   █▀▀▀▀█ █▀▀▀▀       █    █ █   █   ██   █   █
      ██   █    █ █████       ███▀▀  ▀████ ████   ▀████

Welcome to the Dojo

Usage:
    dojo create_room <room_type> <room_name>...
    dojo add_person <person_first_name> <person_last_name> <person_type> [<wants_accommodation>]
    dojo print_room <room_name>
    dojo print_allocations [<filename>]
    dojo print_unallocated [<filename>]
    dojo print_vacant_rooms
    dojo load_people [<filename>]
    dojo get_person_id <person_first_name> <person_last_name>
    dojo reallocate_person <person_id> <room_name>
    dojo load_state [<sqlite_db_name>]
    dojo save_state [<sqlite_db_name>]
    dojo (-i | --interactive)
    dojo (-h | --help)
    dojo (-v | --version)

Options:
    -i, --interactive           :  Interactive Mode
    -h, --help                  :  show this help message
    -v, --version               :  print the version of the system
    create_room                 :  create a room of a certain type
    add_person                  :  add a person to the system
    <room_type>                 :  office or livingspace
    <room_name>                 :  enter a desired room name
    <person_first_name>         :  the first name of the person
    <person_other_name>         :  the other name of the person
    <person_type>               :  indicate whether the person is staff or fellow
    [<wants_accommodation>]     :  'Y' or 'y' if the person wants accommodation, otherwise leave blank
    [<filename>]                :  output or input filename
    [<sqlite_db_name>]          :  name of the database to either load data from or save data to
"""

import sys
import cmd
from docopt import docopt, DocoptExit
from termcolor import cprint
from system.dojo import Dojo

new_dojo = Dojo()


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """

    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print("Invalid Command!")
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class MyInteractive(cmd.Cmd):
    prompt = "Dojo >>> "
    file = None
    print(__doc__)

    @docopt_cmd
    def do_create_room(self, args):
        """Usage: create_room <room_type> <room_name>..."""
        if args["<room_type>"].lower() == "office":
            for i in args["<room_name>"]:
                new_dojo.create_room(i, "office")
        elif args["<room_type>"].lower() == "livingspace":
            for i in args["<room_name>"]:
                new_dojo.create_room(i, "livingspace")
        else:
            cprint(
                "Sorry. Check the room type you entered and try again", "red")

    @docopt_cmd
    def do_add_person(self, args):
        """Usage: add_person <person_first_name> <person_last_name> <person_type> [<wants_accommodation>]"""
        if args["<person_first_name>"] and args["<person_last_name>"]:
            person_first_name = args["<person_first_name>"]
            person_last_name = args["<person_last_name>"]

            if args["<person_type>"].upper() == "FELLOW":
                if args["<wants_accommodation>"] == "Y" or args["<wants_accommodation>"] == "y":
                    wants_accommodation = True
                    p_type = "fellow"
                    new_dojo.add_person(person_first_name, person_last_name, p_type, wants_accommodation)
                    print("")

                elif args["<wants_accommodation>"] is None:
                    wants_accommodation = False
                    p_type = "fellow"
                    new_dojo.add_person(person_first_name, person_last_name, p_type, wants_accommodation)
                    print("")

            elif args["<person_type>"].upper() == "STAFF":
                p_type = "staff"
                new_dojo.add_person(person_first_name, person_last_name, p_type)
                print("")

                if args["<wants_accommodation>"] == "Y" or args[
                       "<wants_accommodation>"] == "y":
                    cprint("Sorry. Staff cannot be allocated to a living space"
                           , "red")

            else:
                cprint("Sorry. Check the person type you entered and try again"
                       , "red")

    @docopt_cmd
    def do_print_room(self, args):
        """Usage: print_room <room_name>"""
        room_name = args["<room_name>"]
        print("")
        new_dojo.print_room(room_name)

    @docopt_cmd
    def do_print_vacant_rooms(self, args):
        """Usage: print_vacant_rooms"""
        new_dojo.print_vacant_rooms()

    @docopt_cmd
    def do_print_allocations(self, args):
        """Usage: print_allocations [<filename>]"""
        if args["<filename>"]:
            filename = args["<filename>"]
            print("")
            new_dojo.print_allocations(filename)
        else:
            print("")
            new_dojo.print_allocations()

    @docopt_cmd
    def do_print_unallocated(self, args):
        """Usage: print_unallocated [<filename>]"""
        if args["<filename>"]:
            filename = args["<filename>"]
            print("")
            new_dojo.print_unallocated(filename)
        else:
            print("")
            new_dojo.print_unallocated()

    @docopt_cmd
    def do_load_people(self, args):
        """Usage: load_people [<filename>]"""
        if args["<filename>"]:
            new_dojo.load_people(args["<filename>"])
        else:
            new_dojo.load_people()

    @docopt_cmd
    def do_get_person_id(self, args):
        """Usage: get_person_id <person_first_name> <person_last_name>"""
        p_name = args["<person_first_name>"] + " " + args["<person_last_name>"]
        new_dojo.get_person_id(p_name)

    @docopt_cmd
    def do_reallocate_person(self, args):
        """Usage: reallocate_person <person_id> <room_name>"""
        p_id = int(args["<person_id>"])
        r_name = args["<room_name>"]
        new_dojo.reallocate_person(p_id, r_name)

    @docopt_cmd
    def do_save_state(self, args):
        """Usage: save_state [<sqlite_db_name>]"""
        if args["<sqlite_db_name>"]:
            new_dojo.save_state(args["<sqlite_db_name>"])
        else:
            new_dojo.save_state()

    @docopt_cmd
    def do_load_state(self, args):
        """Usage: load_state [<sqlite_db_name>]"""
        if args["<sqlite_db_name>"]:
            new_dojo.load_state(db_name=args["<sqlite_db_name>"])
        else:
            new_dojo.load_state()

    @docopt_cmd
    def do_version(self, args):
        """Usage: version"""
        cprint("Version 1.0")

    def do_quit(self, args):
        """Quits out of Interactive Mode."""
        print("Good Bye!")
        exit()

    def do_exit(self, args):
        """Exits the interactive mode"""
        print("Good bye!")
        exit()


opt = docopt(__doc__, sys.argv[1:])

if opt["--interactive"]:
    MyInteractive().cmdloop()

print(opt)
