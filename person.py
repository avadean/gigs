
class Person:
    def __init__(self, name):
        assert isinstance(name, str)

        self._name = name

    def name(self):
        return self._name

    def __eq__(self, other):
        assert isinstance(other, Person)

        return self._name == other._name

    def __repr__(self):
        return self._name

