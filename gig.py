from person import Person
from ticket import Ticket
from utils import get_date

from datetime import datetime


class Gig:
    def __init__(self, name, year=None, month=None, day=None, date=None, tickets=None):
        assert isinstance(name, str)

        if tickets is None:
            tickets = []

        assert isinstance(tickets, (list, set, tuple))
        assert all(isinstance(ticket, Ticket) for ticket in tickets)

        self._name = name
        self._date = get_date(year, month, day, date)
        self._tickets = tickets

    def get_ticket(self, person):
        assert isinstance(person, Person)

        for ticket in self._tickets:
            if ticket.attendee() == person:
                return ticket

        raise ValueError('Could not find a ticket for this person.')

    def add_ticket(self, ticket):
        assert isinstance(ticket, Ticket)

        if any(ticket.attendee() == other_ticket.attendee() for other_ticket in self._tickets):
            raise ValueError('Trying to add ticket for an already attendee.')

        self._tickets.append(ticket)

    def remove_ticket(self, ticket):
        assert isinstance(ticket, Ticket)

        self._tickets.remove(ticket)


    def is_upcoming(self):
        return (self._date is not None) and (datetime.now() < self._date)

    def has_passed(self):
        return (self._date is not None) and (datetime.now() > self._date)

    def all_settled_up(self):
        return all(ticket.settled_up() for ticket in self._tickets)

    def name(self):
        return self._name

    def date(self):
        return self._date


    def __str__(self):
        output = '! ' if not self.all_settled_up() else '  '

        date_suffix = '' if self._date is None else {1: 'st', 2: 'nd', 3: 'rd'}.get(self._date.day % 20, 'th')
        date_output = '' if self._date is None else self._date.strftime('%a %d{date_suffix} %b %Y : ').replace('{date_suffix}', date_suffix)

        name_output = '       *dummy*       ' if not self._name else f'{self._name:^21}'

        output += date_output + name_output + ' -> '

        attendees = [ticket.attendee() for ticket in self._tickets]

        if not attendees:
            attendees_output = '*no attendees*'
        else:
            attendees = sorted([attendee.name() for attendee in attendees])
            num_attendees = len(attendees)

            #num_per_line = 3
            #attendees_split = [attendees[n:n+num_per_line] for n in range(num_attendees // num_per_line)] + [attendees[-(num_attendees % num_per_line):]]
            #attendees_split_max = max(max(len(att) for att in lst) for lst in attendees_split)
            #attendees_string = '{:' + str(attendees_split_max) + '}        '
            #attendees_output = ('\n' + (' ' * len(output))).join([(attendees_string * len(split)).format(*split) for split in attendees_split])

            attendees_output = f'{num_attendees} {"person" if num_attendees == 1 else "people"} : ' + ' - '.join(attendees)

        output += attendees_output

        return output

