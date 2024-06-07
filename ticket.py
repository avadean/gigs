from person import Person


class Ticket:
    def __init__(self, attendee, buyer=None, price=None, settled_up=True):
        assert isinstance(attendee, Person)

        if buyer is None:
            buyer = attendee

        assert isinstance(buyer, Person)

        if price is not None:
            assert isinstance(price, (float, int))

            price = float(price)

            assert price >= 0.0

        assert isinstance(settled_up, bool)
        assert not (buyer == attendee and not settled_up)

        self._attendee = attendee
        self._buyer = buyer
        self._price = price
        self._settled_up = settled_up

    def attendee(self):
        return self._attendee

    def buyer(self):
        return self._buyer

    def price(self):
        return self._price

    def settle_up(self):
        if self._settled_up:
            raise ValueErorr('Ticket already settled up.')

        self._settled_up = True

    def settled_up(self):
        return self._settled_up

    def _key(self):
        return (self._attendee, self._buyer, self._settled_up)

    def __hash(self):
        return hash(self._key())

    def __eq__(self, other):
        assert isinstance(other, Ticket)

        return self._key() == other._key()

    def __str__(self):
        output = f'TICKET ->\n  Attendee: {self._attendee}'

        if self._attendee != self._buyer:
            output += f'\n  Buyer:    {self._buyer}'
            output += '' if self._price is None else f'\n  £{round(self._price, 2)}'
            output += f'\n  Settled up? {"y" if self._settled_up else "n"}'

        return output
