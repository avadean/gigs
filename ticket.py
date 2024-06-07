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

    @property
    def attendee(self):
        return self._attendee

    @attendee.setter
    def attendee(self, value):
        assert isinstance(value, Person)

        self._attendee = value

    @property
    def buyer(self):
        return self._buyer

    @buyer.setter
    def buyer(self, value):
        assert isinstance(value, Person)

        self._buyer = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value is not None:
            assert isinstance(value, (float, int))

            value = float(value)

            assert value >= 0.0

        self._price = value

    def settle_up(self):
        self.settled_up = True

    @property
    def settled_up(self):
        return self._settled_up

    @settled_up.setter
    def settled_up(self, value):
        assert isinstance(value, bool)
        print('through setter')

        if value and self._settled_up:
            raise ValueError('Ticket already settled up.')

        self._settled_up = value

    def _key(self):
        return (self._attendee, self._buyer, self._settled_up)

    def __hash(self):
        return hash(self._key())

    def __eq__(self, other):
        assert isinstance(other, Ticket)

        return self._key() == other._key()

    def __repr__(self):
        return str(self._attendee)

    def __str__(self):
        output = f'TICKET ->\n  Attendee: {self._attendee}'

        if self._attendee != self._buyer:
            output += f'\n  Buyer:    {self._buyer}'
            output += '' if self._price is None else f'\n  £{round(self._price, 2)}'
            output += f'\n  Settled up? {"y" if self._settled_up else "n"}'

        return output
