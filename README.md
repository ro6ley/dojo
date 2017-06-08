[![Coverage Status](https://coveralls.io/repos/github/NaiRobley/dojo/badge.svg?branch=develop)](https://coveralls.io/github/NaiRobley/dojo?branch=develop)
[![Build Status](https://travis-ci.org/NaiRobley/dojo.svg?branch=develop)](https://travis-ci.org/NaiRobley/dojo)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/4d579665683f41088688d2cad5de8d17)](https://www.codacy.com/app/NaiRobley/dojo?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=NaiRobley/dojo&amp;utm_campaign=Badge_Grade)

# Project - Andela Office Space Allocation  

When a new Fellow joins Andela they are assigned an office space and an optional living space if
they choose to opt in.
When a new Staff joins they are assigned an office space only.
This project will digitize and randomize a room allocation system for one of
Andela Kenya’s facilities called The Dojo.
This system will be used to automatically allocate spaces to people at random.


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

The requirements are in the file

```
requirements.txt
```

### Installing

Install python in your system if you don't have it yet (Why though?)
```
$ sudo apt install python
```

Clone the repo:
HTTPS
```
$ git clone https://github.com/NaiRobley/dojo.git
```
SSH
```
$ git clone git@github.com:NaiRobley/dojo.git
```

Change Directory into the project folder
```
$ cd dojo
```

Create a virtual environment with Python 3.5
```
$ virtualenv --python=python3.5 yourenvname
```

Activate the virtual environment you have just created
```
$ source yourenvname/bin/activate
```

Install the application's dependencies from requirements.txt to the virtual environment
```
$ (yourenvname) pip install -r requirements.txt
```

Run the tool in interactive mode:
```
$ (yourenvname) python main.py -i
```

Usage:
```
    create_room <room_type> <room_name>...
    add_person <person_first_name> <person_last_name> <person_type> [<wants_accommodation>]
    print_room <room_name>
    print_allocations [<filename>]
    print_unallocated [<filename>]
    load_people [<filename>]
    get_person_id <person_first_name> <person_last_name>
    reallocate_person <person_id> <room_name>
    print_vacant_rooms
    delete_room <room_name>
    remove_person <person_id>
    rename_room <room_name> <new_room_name>
    rename_person <person_id> <new_first_name> <new_last_name>
    load_state [<sqlite_db_name>]
    save_state [<sqlite_db_name>]
    help
```
Options:
```
    help                        :  show this help message
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
```

**Contributions are highly welcomed and appreciated**

## Deployment
Coming soon

## Libraries
[Docopt](https://github.com/docopt/docopt) - Docopt helps you create most beautiful command-line interfaces

## Authors

* **Robley Gori**


## License


## Acknowledgments

* The Internet

## Additional resources
Coming soon
