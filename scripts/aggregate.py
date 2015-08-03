import csv

def make_castrow(rowtypes=None):
    '''This function takes e.g. a CSV row of data and casts the data to
    relevant types.

    Imagine this being part of data package utilities
    '''
    if rowtypes is None:
        rowtypes = {
            'amount': 'number'
            }

    def castrow(row):
        for key in rowtypes:
            fieldtype = rowtypes[key]
            if fieldtype != 'string':
                operator = str
                if fieldtype == 'number':
                    operator = float
                row[key] = operator(row[key])
        return row

    return castrow

def aggregate(reader, aggregate_by=None, sumon='amount', castrow=make_castrow()):
    '''
    reader: should yield rows of dictionaries

    @output: a dictionary keyed by tuple of aggregate_by values and value being
    total
    '''
    output = {}
    for row in reader:
        newrow = castrow(row)    
        keyrows = tuple([ newrow[key] for key in aggregate_by ])
        # are the key rows already in output
        output[keyrows] = output.get(keyrows, 0) + newrow[sumon]
    return output


def test_makecastrow():
    caster = make_castrow()
    out = caster({'amount': '10.0'})
    assert out == {'amount': 10.0}

if __name__ == '__main__':
    sumon = 'amount'

    fo = open('data/cra.csv')
    reader = csv.DictReader(fo)
    aggregate_by = [ 'cofog_level1_code' ]
    out = aggregate(reader, aggregate_by)
    print out

    fo = open('data/cra.csv')
    reader = csv.DictReader(fo)
    aggregate_by = [ 'dept_code' ]
    out = aggregate(reader, aggregate_by)
    print out

    # let's get fancy and join on departments
    departments = dict([x for x in csv.reader(open('data/departments.csv'))])
    dep_aggregates = ['dept_code', 'label', 'amount']
    dep_aggregates += [ [k[0], departments[k[0]], v] for k,v in out.items() ]
    import pprint
    pprint.pprint(dep_aggregates)

