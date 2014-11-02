Scripts for processing PESA and CRA data.

## Usage

To use this package you will need to have [Python](http://python.org),
[pip](http://www.pip-installer.org).

Install the dependencies:

    # Assume we are in the base directory (i.e. parent of this directory)

    # We recommend doing this in a virtualenv
    pip install -r scripts/requirements.txt

You can then run the conversion from Excel files to flat CSV by running:

    python script/process.py csvexport

This will generate an output csv file at:

    data/cra.csv

This command may complain that you don't have all the data files you need. In
particular, the ~5MB CRA data files are not included in this repository, and
you will need to download them as per the instructions in the error message.

