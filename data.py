from gig import Gig
from person import Person
from schedule import Schedule
from ticket import Ticket

from datetime import datetime
from pathlib import Path
from pickle import dump as pickle_save, load as pickle_load
from shutil import copy as shutil_copy, move as shutil_move


PEOPLE_FILE = 'people.bin'
DATA_FILE = 'save.bin'
BACKUP_DIR = 'backup_saves/'


class People:
    def __init__(self, people):
        assert isinstance(people, dict)
        assert all(isinstance(key, str) for key in people.keys())
        assert all(isinstance(value, Person) for value in people.values())

        for key, value in people.items():
            setattr(self, key, value)


def get_example_schedule(people):

    # Some initial gigs to create a schedule.
    gigs = [
        Gig('Foo Fighters',
            year=2024, month=6, day=13,
            tickets=[Ticket(people.ava, buyer=people.tom),
                     Ticket(people.alex, buyer=people.tom),
                     Ticket(people.tom),
                     Ticket(people.jake),
                     Ticket(people.jake_dad),
                     Ticket(people.milo),
                     Ticket(people.milo_sister)]),

        Gig('Download Festival',
            year=2024, month=6, day=16,
            tickets=[Ticket(people.ava),
                     Ticket(people.alex, buyer=people.ava),
                     Ticket(people.jake, buyer=people.ava),
                     Ticket(people.siobhan, buyer=people.ava)]),

        Gig('Green Day',
            year=2024, month=6, day=21,
            tickets=[Ticket(people.ava, buyer=people.alex),
                     Ticket(people.alex),
                     Ticket(people.jake, buyer=people.alex)]),

        Gig('Leeds Festival',
            year=2024, month=8, day=24,
            tickets=[Ticket(people.ava),
                     Ticket(people.alex, buyer=people.ava),
                     Ticket(people.tom),
                     Ticket(people.siobhan),
                     Ticket(people.jake, buyer=people.siobhan),
                     Ticket(people.milo)]),

        Gig('Slipknot',
            year=2024, month=12, day=17,
            tickets=[Ticket(people.ava),
                     Ticket(people.alex, buyer=people.ava),
                     Ticket(people.jake),
                     Ticket(people.lewis, buyer=people.jake),
                     Ticket(people.josh),
                     Ticket(people.siobhan, buyer=people.josh)]),

        Gig('Olivia Rodrigo',
            tickets=[Ticket(people.ava)]),

        Gig('Four Year Strong',
            year=2025, month=2, day=19,
            tickets=[Ticket(people.ava),
                     Ticket(people.tom, buyer=people.ava),
                     Ticket(people.jake),
                     Ticket(people.alex, buyer=people.jake)])
    ]


    # Create the schedule.
    return Schedule(gigs)


def load_people(file=PEOPLE_FILE):
    with open(PEOPLE_FILE, 'rb') as people_file:
        people = pickle_load(people_file)

    return people


def load_info(file=DATA_FILE, strict=False):

    if Path(file).exists():
        with open(file, 'rb') as data_file:
            schedule, people = pickle_load(data_file)

    elif not strict:
        people = load_people()
        schedule = get_example_schedule(people)

    else:
        raise FileNotFoundError(f'Could not find file {file}.')

    return schedule, people


def save_info(schedule, people, file=DATA_FILE, verbose=False):
    assert isinstance(schedule, Schedule)
    assert isinstance(people, People)

    if verbose:
        print(f'Saving info to {file}.')

    if Path(file).exists():
        data_file_backup = file + '.bak'

        if Path(data_file_backup).exists():
            if verbose:
                print(f'Moved back up file {data_file_backup} to {BACKUP_DIR}.')

            Path(BACKUP_DIR).mkdir(exist_ok=True)

            shutil_move(data_file_backup, BACKUP_DIR + data_file_backup + str(int(datetime.now().timestamp())))

        if verbose:
            print(f'Made backup of {file} to {data_file_backup}.')

        shutil_copy(file, data_file_backup)

    with open(file, 'wb') as data_file:
        pickle_save((schedule, people), data_file)


if __name__ == '__main__':

    # Usually only run data as main when wanting to manually edit saved versions of people.
    people = load_people()

