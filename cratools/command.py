import json
import logging
import optparse
import os
import sys

log = logging.getLogger('cratools')

log.addHandler(logging.StreamHandler(sys.stderr))
log.setLevel(logging.WARN)

repo_root = os.path.dirname(os.path.dirname(__file__))

class MissingDataFile(Exception): pass

class Config(object):
    def __init__(self, fileobj):
        self.data = json.load(fileobj)
        self.data['data_dir'] = os.path.join(repo_root, 'data')
        self.data['archive_dir'] = os.path.join(repo_root, 'archive')

    def data_file(self, name, filedir=None):
        filedir = filedir or self.data['data_dir']
        fname = os.path.join(filedir, name)
        try:
            return file(fname)
        except IOError:
            raise MissingDataFile("The data file '%s' is missing. Please download " \
                                  "it\nand place it at\n  %s" \
                                  % (name, fname))

    def archive_file(self, name):
        return self.data_file(name, filedir=self.data['archive_dir'])

parser = optparse.OptionParser("cratools csvexport")
parser.add_option('-v', '--verbose', action='count', dest='verbose', default=0)

def main():
    opts, args = parser.parse_args()
    log.setLevel(max(10, log.getEffectiveLevel() - 10 * opts.verbose))

    config_file = file(os.path.join(repo_root, 'datapackage.json'))
    config = Config(config_file)

    if len(args) != 1 or args[0] != 'csvexport':
        parser.print_help()
        return 1

    from cra import cra2010_clean
    out = file('data/cra.csv', 'w')
    # out=sys.stdout
    cra2010_clean(config, out=out)

