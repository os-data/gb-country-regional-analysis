import csv
import logging
import sys

log = logging.getLogger(__name__)

class Cofog(object):
    def __init__(self, data_file, dejargonise_file=None):
        self.data_file = data_file
        self.dejargonise_file = dejargonise_file

        self.data = {}
        self._load()

        if self.dejargonise_file:
            self._dejargonise()
        else:
            log.warn("Not dejargonising COFOG codes, as no dejargonise_file provided")

        self._promote_notes()

    def __getitem__(self, key):
        return self.data[key]

    def _load(self):
        """Do initial load of COFOG csv file into internal data structure."""
        reader = csv.reader(self.data_file)
        header = reader.next() # Code, Title, Details, Change date

        for row in reader:
            code, description, explanatory_note, change_date = [unicode(x, 'UTF-8') for x in row]

            self.data[code] = {
                'code': code,
                'description': description,
                'explanatory_note': explanatory_note,
                'change_date': change_date
            }

            parts = code.split('.')
            parents = [u'.'.join(parts[:i+1]) for i, _ in enumerate(parts)]

            if len(parents) == 1:
                self.data[code]['level'] = 1
            elif len(parents) == 2:
                self.data[code]['parent'] = parents[0]
                self.data[code]['level'] = 2
            elif len(parents) == 3:
                self.data[code]['parent'] = parents[1]
                self.data[code]['level'] = 3
            else:
                raise ValueError("COFOG code has too many or too few parents: %s, parents %s" \
                                 % (code, parents))


    def _dejargonise(self):
        '''
        Replaces offical descriptions for COFOG codes, with more sensible ones
        chosen specially for WDMMG.

        Taken from Google Spreadsheet at http://bit.ly/qN85xj
        '''
        exp_num_columns = 5

        reader = csv.reader(self.dejargonise_file)
        reader.next() # skip header
        reader.next() # skip notes

        for row in reader:
            code, official, alternative, color, notes, _, _, _ = [unicode(x, 'UTF-8') for x in row]

            if not code in self.data.keys():
                raise ValueError("Found unknown COFOG code in dejargonize mapping ('%s'). "\
                                 "Is the mapping up to date?" % code)

            if alternative:
                log.debug("Replacing description on %s ('%s' -> '%s')", code, self.data[code]['description'], alternative)
                self.data[code]['official_description'] = self.data[code]['description']
                self.data[code]['description'] = alternative

            if color:
                self.data[code]['color'] = color

            # TODO: replace explanatory_note as well?

    def _promote_notes(self):
        '''
        Where a level 2 COFOG code has exactly one level 3 sub-code, there is
        often no detailed description for the level 2 code. This method will
        supply the missing description by copying it from the level 3 sub-code.
        '''
        for code, data in self.data.iteritems():
            if data['level'] != 2:
                continue

            if data.get('explanatory_note'):
                continue

            def _is_possible_child(child):
                child_code, child_data = child
                code_match = child_code.startswith(code)
                level_match = child_data['level'] == 3
                return code_match and level_match

            possible_children = filter(_is_possible_child, self.data.iteritems())

            if len(possible_children) != 1:
                continue

            child_code, child_data = possible_children[0]

            if child_data.get('explanatory_note'):
                log.debug("Copying notes from %s to %s", child_code, code)
                data['explanatory_note'] = child_data['explanatory_note']

