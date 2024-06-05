from gig import Gig
from person import Person
from schedule import Schedule
from ticket import Ticket

from datetime import datetime
from pathlib import Path
from pickle import dump as pickle_save, load as pickle_load
from shutil import copy as shutil_copy, move as shutil_move

DATA_FILE = 'save.bin'
BACKUP_DIR = 'backup_saves/'


# Add people here.
ava = Person('Ava')
alex = Person('Alex')
jake = Person('Jake')
jake_dad = Person('Jake dad')
ebony = Person('Ebony')
siobhan = Person('Siobhan')
josh = Person('Josh')
milo = Person('Milo')
milo_sister = Person('Milo sister')
tom = Person('Tom')
lewis = Person('Lewis')
kate = Person('Kate')
dan = Person('Dan')
preston = Person('Preston')
sophie = Person('Sophie')


def get_example_schedule():

    # Some initial gigs to create a schedule.
    gigs = [
        Gig('Foo Fighters',
            year=2024, month=6, day=13,
            tickets=[Ticket(ava, buyer=tom),
                     Ticket(alex, buyer=tom),
                     Ticket(tom),
                     Ticket(jake),
                     Ticket(jake_dad),
                     Ticket(milo),
                     Ticket(milo_sister)]),

        Gig('Download Festival',
            year=2024, month=6, day=16,
            tickets=[Ticket(ava),
                     Ticket(alex, buyer=ava),
                     Ticket(jake, buyer=ava),
                     Ticket(siobhan, buyer=ava)]),

        Gig('Green Day',
            year=2024, month=6, day=21,
            tickets=[Ticket(ava, buyer=alex),
                     Ticket(alex),
                     Ticket(jake, buyer=alex)]),

        Gig('Leeds Festival',
            year=2024, month=8, day=24,
            tickets=[Ticket(ava),
                     Ticket(alex, buyer=ava),
                     Ticket(tom),
                     Ticket(siobhan),
                     Ticket(jake, buyer=siobhan),
                     Ticket(milo)]),

        Gig('Slipknot',
            year=2024, month=12, day=17,
            tickets=[Ticket(ava),
                     Ticket(alex, buyer=ava),
                     Ticket(jake),
                     Ticket(lewis, buyer=jake),
                     Ticket(josh),
                     Ticket(siobhan, buyer=josh)]),

        Gig('Olivia Rodrigo',
            tickets=[Ticket(ava)]),

        Gig('Four Year Strong',
            year=2025, month=2, day=19,
            tickets=[Ticket(ava),
                     Ticket(tom, buyer=ava),
                     Ticket(jake),
                     Ticket(alex, buyer=jake)])
    ]


    # Create the schedule.
    return Schedule(gigs)


def load_schedule(file=DATA_FILE, strict=False):

    if Path(file).exists():
        with open(file, 'rb') as data_file:
            schedule = pickle_load(data_file)

        return schedule

    elif not strict:
        return get_example_schedule()

    else:
        raise FileNotFoundError(f'Could not find file {file}.')


def save_schedule(schedule, file=DATA_FILE, verbose=False):
    if verbose:
        print(f'Saving schedule to {file}.')

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
        pickle_save(schedule, data_file)


if __name__ == '__main__':
    save_schedule(get_example_schedule)

