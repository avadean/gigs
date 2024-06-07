
class Person:
    def __init__(self, name):
        assert isinstance(name, str)

        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        assert isinstance(value, str)

        self._name = value

    def _key(self):
        return (self._name,)

    def __eq__(self, other):
        assert isinstance(other, Person)

        return self._key() == other._key()

    def __str__(self):
        return self._name

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self._key())

