import re

class CRACofogMapper(object):
    '''
    In the published data, the "function" and "subfunction" columns are used
    inconsistently. This is partly because some departments continue to use a
    previous coding system, and partly because only two columns have been
    allowed for the three levels of the COFOG hierarchy.

    This class uses a mapping provided by William Waites to work out the
    correct COFOG code, given the published data.
    '''
    def __init__(self, mappings):
        '''
        Constructs a COFOG mapper from a mappings object (which is
        usually loaded from a JSON file).

        mappings - a list of triples. In each
            triple, the first element is the good code, and the second and
            third elements give the published values. If the first element
            (the good code) contains non-numerical suffix, it will be removed.
        '''
        self.mappings = {}
        for good, bad1, bad2 in mappings:
            good = re.match(r'([0-9]+(\.[0-9])*)', good).group(1)
            self.mappings[bad1, bad2] = good

    def fix(self, function, subfunction):
        '''
        Looks up the fixed COFOG code given the published values.

        Returns a list giving all available COFOG levels, e.g.
        `[u'01', u'01.1', u'01.1.1']`

        Returns an empty list if no COFOG mapping has been
        defined.
        '''
        ans = self.mappings.get((function, subfunction))
        if ans is None:
            return []
        parts = ans.split('.')
        return ['.'.join(parts[:i+1]) for i, _ in enumerate(parts)]
