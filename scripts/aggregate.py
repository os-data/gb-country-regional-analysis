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


def doitall(aggregate_by, outname):
    fo = open('data/cra.csv')
    reader = csv.DictReader(fo)
    out = aggregate(reader, aggregate_by)

    # ok so where do headings come from - and do we need them?
    outrows = [aggregate_by + ['value']]
    outrows += [ [x for x in key] + [value] for key, value in out.items() ]

    fo = open('aggregates/%s.csv' % outname, 'w')
    writer = csv.writer(fo)
    writer.writerows(outrows)

def test_makecastrow():
    caster = make_castrow()
    out = caster({'amount': '10.0'})
    assert out == {'amount': 10.0}

def test_aggregate():
    fo = open('data/cra.csv')
    reader = csv.DictReader(fo)
    aggregate_by = [ 'cofog_level1_code' ]
    out = aggregate(reader, aggregate_by)

    fo = open('data/cra.csv')
    reader = csv.DictReader(fo)
    aggregate_by = [ 'cofog_level1_code', 'dept_code' ]
    out = aggregate(reader, aggregate_by)
    print sorted(out.keys())
    print out[('02', 'Dept010')]
    assert out[('02', 'Dept010')] == 10844376000.0


if __name__ == '__main__':
    doitall(['dept_code'], 'by-department')

    doitall(['cofog_level1_code', 'dept_code'], 'by-cofog1-then-department')


    # join example
    fo = open('data/cra.csv')
    reader = csv.DictReader(fo)
    aggregate_by = [ 'dept_code' ]
    out = aggregate(reader, aggregate_by)

    # let's get fancy and join on departments
    departments = dict([x for x in csv.reader(open('data/departments.csv'))])
    dep_aggregates = ['dept_code', 'label', 'amount']
    dep_aggregates += [ [k[0], departments[k[0]], v] for k,v in out.items() ]
    import pprint
    # pprint.pprint(dep_aggregates)

    # fo = open('aggregates/by-department.csv', 'w')
    # writer = csv.writer(fo)
    # writer.writerows(dep_aggregates)
