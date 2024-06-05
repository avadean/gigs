from gig import Gig


class Schedule:
    def __init__(self, gigs=None):
        if gigs is None:
            gigs = []

        assert isinstance(gigs, (list, set, tuple))
        assert all(isinstance(gig, Gig) for gig in gigs)

        self._gigs = gigs

    def add_gig(self, gig):
        assert isinstance(gig, Gig)

        self._gigs.append(gig)

    def get_gig(self, gig_name, gig_type='any'):
        assert isinstance(gig_name, str)
        assert isinstance(gig_type, str)
        assert gig_type in ('any', 'upcoming', 'passed', 'none')

        upcoming_gigs, passed_gigs, no_date_gigs = self._organise_gigs()

        if gig_type in ('any', 'upcoming'):
            for other_gig in upcoming_gigs:
                if other_gig.name() == gig_name:
                    return other_gig

        if gig_type in ('any', 'passed'):
            for other_gig in passed_gigs:
                if other_gig.name() == gig_name:
                    return other_gig

        if gig_type in ('any', 'none'):
            for other_gig in no_date_gigs:
                if other_gig.name() == gig_name:
                    return other_gig

        raise ValueError(f'Could not find gig with name {gig_name}.')

    def next_gig(self):
        upcoming_gigs, passed_gigs, no_date_gigs = self._organise_gigs()

        if not upcoming_gigs:
            return None

        return upcoming_gigs[0]

    def _organise_gigs(self):
        upcoming_gigs = sorted([gig for gig in self._gigs if gig.is_upcoming()], key=lambda gig: gig.date())
        passed_gigs = sorted([gig for gig in self._gigs if gig.has_passed()], key=lambda gig: gig.date(), reverse=True)
        no_date_gigs = sorted([gig for gig in self._gigs if gig.date() is None], key=lambda gig: gig.name())

        return upcoming_gigs, passed_gigs, no_date_gigs

    def __str__(self):
        if not self._gigs:
            return '*no gigs scheduled*'

        upcoming_gigs, passed_gigs, no_date_gigs = self._organise_gigs()

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

