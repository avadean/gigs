from person import Person


class Ticket:
    def __init__(self, attendee, buyer=None, settled_up=True):
        assert isinstance(attendee, Person)

        if buyer is None:
            buyer = attendee

        assert isinstance(buyer, Person)
        assert isinstance(settled_up, bool)
        assert not (buyer == attendee and not settled_up)

        self._attendee = attendee
        self._buyer = buyer
        self._settled_up = settled_up

    def attendee(self):
        return self._attendee

    def buyer(self):
        return self._buyer

    def settle_up(self):
        if self._settled_up:
            raise ValueErorr('Ticket already settled up.')

        self._settled_up = True

    def settled_up(self):
        return self._settled_up

    def __str__(self):
        output = f'TICKET ->\n  Attendee: {self._attendee}'

        if self._attendee != self._buyer:
            output += '\n  Buyer:    {self._buyer}\n  Settled up? {"y" if self._settled_up else "n"}'

        return output
