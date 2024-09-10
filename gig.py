from person import Person
from ticket import Ticket
from utils import day_suffix, get_date

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
        self._tickets = []

        for ticket in tickets:
            self.add_ticket(ticket)

    def get_ticket_of(self, person):
        assert isinstance(person, Person)

        for ticket in self._tickets:
            if ticket.attendee == person:
                return ticket

        raise ValueError('Could not find a ticket for this person.')

    def add_ticket(self, ticket):
        assert isinstance(ticket, Ticket)

        if any(ticket.attendee == other_ticket.attendee for other_ticket in self._tickets):
            raise ValueError('Trying to add ticket for an already attendee.')

        self._tickets.append(ticket)

    def remove_ticket(self, ticket):
        assert isinstance(ticket, Ticket)

        self._tickets.remove(ticket)

    def ticket_summary(self):

        if not self._tickets:
            raise ValueError('No tickets allocated to this gig.')

        buyers = list({ticket.buyer for ticket in self._tickets})
        num_buyers = len(buyers)

        attendees = [ticket.attendee for ticket in self._tickets]
        num_attendees = len(attendees)

        date_suffix = '' if self._date is None else day_suffix(self._date.day)
        date_output = '' if self._date is None else self._date.strftime('%a %d{date_suffix} %b %Y : ').replace('{date_suffix}', date_suffix)

        name_output = ' *dummy* ' if not self._name else self._name

        output = 'TICKETS -> ' + date_output + name_output

        # Create a dictionary where each buyer has a list of the attendees they've bought tickets for (including themself if so).
        buyer_to_attendee = {buyer: [ticket.attendee for ticket in self._tickets if ticket.buyer == buyer] for buyer in buyers}

        # Order alphabetically by buyer.
        buyer_to_attendee = dict(sorted(buyer_to_attendee.items(), key=lambda buyer_attendee: buyer_attendee[0].name))

        # Reorder the attendees to place the buyer at the front for printing convenience later.
        buyer_to_attendee = {buyer: sorted(attendees_of_this_buyer,
                                           key=lambda attendee: (attendee != buyer, attendee.name)) for buyer, attendees_of_this_buyer in buyer_to_attendee.items()}

        for buyer, attendees_of_this_buyer in buyer_to_attendee.items():
            output += '\n'
            output += '  ' + ('{:^' + str(max(len(str(buyer)) for buyer in buyers) + 2) + '} has bought tickets for : ').format(str(buyer))
            output += ' - '.join(map(str, attendees_of_this_buyer))

        if not self.all_settled_up():
            output += '\n\nSETTLE UPS ->'

            for ticket in self._tickets:
                if not ticket.settled_up:
                    output += f'\n  {ticket.attendee} owes {ticket.buyer} £{round(ticket.price()) if ticket.price() is not None else "??"} for their ticket.'

        return output


    def is_upcoming(self):
        return (self._date is not None) and (datetime.now() < self._date)

    def has_passed(self):
        return (self._date is not None) and (datetime.now() > self._date)

    def all_settled_up(self):
        return all(ticket.settled_up for ticket in self._tickets)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        assert isinstance(value, str)

        self._name = value

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        if value is not None:
            assert isinstance(value, datetime)

        self._date = datetime

    @staticmethod
    def get_date(year, month, day):
        return get_date(year, month, day)

    @property
    def tickets(self):
        return self._tickets

    @tickets.setter
    def tickets(self, value):
        assert isinstance(value, (list, set, tuple))

        self._tickets = []

        for ticket in value:
            self.add_ticket(ticket)


    def _key(self):
        return (self._name, self._date, self._tickets)

    def __hash(self):
        return hash(self._key())

    def __eq__(self, other):
        assert isinstance(other, Gig)

        return self._key() == other._key()

    def __iter__(self):
        for ticket in self._tickets:
            yield ticket

    def __repr__(self):
        return self._name + ((' - {}'.format(self._date.strftime('%b %Y'))) if self._date is not None else '')

    def __str__(self):
        output = '! ' if not self.all_settled_up() else '  '

        date_suffix = '' if self._date is None else day_suffix(self._date.day)
        date_output = '' if self._date is None else self._date.strftime('%a %d{date_suffix} %b %Y : ').replace('{date_suffix}', date_suffix)

        name_output = '       *dummy*       ' if not self._name else f'{self._name:^21}'

        output += date_output + name_output

        attendees = [ticket.attendee for ticket in self._tickets]
        attendees_output = ''

        if attendees:
            attendees_output += ' -> '
            attendees = sorted([attendee.name for attendee in attendees])
            num_attendees = len(attendees)

            #num_per_line = 3
            #attendees_split = [attendees[n:n+num_per_line] for n in range(num_attendees // num_per_line)] + [attendees[-(num_attendees % num_per_line):]]
            #attendees_split_max = max(max(len(att) for att in lst) for lst in attendees_split)
            #attendees_string = '{:' + str(attendees_split_max) + '}        '
            #attendees_output += ('\n' + (' ' * len(output))).join([(attendees_string * len(split)).format(*split) for split in attendees_split])

            attendees_output += f'{num_attendees:>2} {"person" if num_attendees == 1 else "people"} : ' + ' - '.join(attendees)

        output += attendees_output

        return output

