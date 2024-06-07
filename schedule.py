from gig import Gig
from utils import get_date


class Schedule:
    def __init__(self, gigs=None):
        if gigs is None:
            gigs = []

        assert isinstance(gigs, (list, set, tuple))
        assert all(isinstance(gig, Gig) for gig in gigs)

        self._gigs = gigs

    @property
    def gigs(self):
        return self._gigs

    def add_gig(self, gig):
        assert isinstance(gig, Gig)

        upcoming_gigs, passed_gigs, no_date_gigs = organise_gigs(self._gigs)

        if gig.date is None:
            # We're trying to add a gig with no date, so only check no_date_gigs.

            for other_gig in no_date_gigs:
                if other_gig.name == gig.name:
                    raise ValueError('Trying to add a no date gig that already exists.')

        else:
            # We've been given a specific date, so be more strict with equality checks.

            for other_gig in upcoming_gigs:
                if (other_gig.name == gig.name) and (other_gig.date == gig.date):
                    raise ValueError('Trying to add upcoming gig that already exists.')

            for other_gig in passed_gigs:
                if (other_gig.name == gig.name) and (other_gig.date == gig.date):
                    raise ValueError('Trying to add passed gig that already exists.')

        self._gigs.append(gig)

    def remove_gig(self, gig):
        assert isinstance(gig, Gig)

        self._gigs.remove(gig)

    def get_gig(self, gig_name, year=None, month=None, day=None, date=None):
        assert isinstance(gig_name, str)

        # If a specific date is asked for then the equalities will be strict.
        # Otherwise (i.e all of year, month, day, date are None) the equalities will only check the names of gigs.
        gig_date = get_date(year, month, day, date)

        upcoming_gigs, passed_gigs, no_date_gigs = organise_gigs(self._gigs)

        if gig_date is None:
            # If no gig date, then look at no_date_gigs first.

            for other_gig in no_date_gigs:
                if other_gig.name == gig_name:
                    return other_gig


        # Either no date given or a no date gig was not found, so keep checking - upcoming gigs first then passed.

        for other_gig in upcoming_gigs:
            if (other_gig.name == gig_name) and (gig_date is None or (other_gig.date == gig_date)):
                return other_gig

        for other_gig in passed_gigs:
            if (other_gig.name == gig_name) and (gig_date is None or (other_gig.date == gig_date)):
                return other_gig

        raise ValueError(f'Could not find gig with name {gig_name}.')

    def next_gig(self):
        upcoming_gigs, passed_gigs, no_date_gigs = organise_gigs(self._gigs)

        if not upcoming_gigs:
            return None

        return upcoming_gigs[0]


    def __iter__(self):
        for gig in self._gigs:
            yield gig

    def __in__(self, gig):
        assert isinstance(gig, Gig)

        return gig in self._gigs

    def __str__(self):
        if not self._gigs:
            return '*no gigs scheduled*'

        upcoming_gigs, passed_gigs, no_date_gigs = organise_gigs(self._gigs)

        output = ''

        if upcoming_gigs:
            output += '\nUPCOMING GIGS ->\n  ' + '\n  '.join(map(str, upcoming_gigs)) + '\n'

        if passed_gigs:
            output += '\nPASSED GIGS ->\n  ' + '\n  '.join(map(str, passed_gigs)) + '\n'

        if no_date_gigs:
            output += '\nOTHER GIGS ->\n  ' + '\n  '.join(map(str, no_date_gigs)) + '\n'

        if not output:
            output += '*empty schedule*'

        return output



def organise_gigs(gigs):
    assert isinstance(gigs, (list, set, tuple))

    upcoming_gigs = sorted([gig for gig in gigs if gig.is_upcoming()], key=lambda gig: gig.date)
    passed_gigs = sorted([gig for gig in gigs if gig.has_passed()], key=lambda gig: gig.date, reverse=True)
    no_date_gigs = sorted([gig for gig in gigs if gig.date is None], key=lambda gig: gig.name)

    return upcoming_gigs, passed_gigs, no_date_gigs

