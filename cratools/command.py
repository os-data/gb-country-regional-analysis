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
        self.data['data_dir'] = self.data['data_dir'].format(repo_root=repo_root)

    def data_file(self, name):
        fconf = self.data['data_files'][name]
        fname = os.path.join(self.data['data_dir'], fconf['path'])
        try:
            return file(fname)
        except IOError:
            raise MissingDataFile("The data file '%s' is missing. Please download " \
                                  "it from\n  %s\nand place it at\n  %s" \
                                  % (name, fconf['url'], fname))

parser = optparse.OptionParser("cratools csvexport")
parser.add_option('-v', '--verbose', action='count', dest='verbose', default=0)

def main():
    opts, args = parser.parse_args()
    log.setLevel(max(10, log.getEffectiveLevel() - 10 * opts.verbose))

    config_file = file(os.path.join(repo_root, 'config.json'))
    config = Config(config_file)

    if len(args) != 1 or args[0] != 'csvexport':
        parser.print_help()
        return 1

    from cra import cra2010_clean
    cra2010_clean(config, out=sys.stdout)

